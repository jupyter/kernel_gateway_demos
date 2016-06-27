# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
import json

from notebook.base.handlers import APIHandler, IPythonHandler, json_errors
from notebook.utils import url_path_join

from tornado import gen, web
from tornado.concurrent import Future
from tornado.ioloop import IOLoop
from tornado.websocket import WebSocketHandler, websocket_connect
from tornado.httpclient import HTTPRequest, HTTPError
from tornado.escape import json_encode, json_decode, url_escape

from ipython_genutils.py3compat import cast_unicode
from jupyter_client.session import Session
from traitlets import Unicode, default
from traitlets.config.configurable import LoggingConfigurable

# TODO: Find a better way to specify global configuration options 
# for a server extension.
KG_URL = os.getenv('KG_URL', 'http://127.0.0.1:8888/')
KG_HEADERS = json.loads(os.getenv('KG_HEADERS', '{}'))
KG_HEADERS.update({
    'Authorization': 'token {}'.format(os.getenv('KG_AUTH_TOKEN', ''))
})


class WebSocketChannelsHandler(WebSocketHandler, IPythonHandler):

    def set_default_headers(self):
        """Undo the set_default_headers in IPythonHandler

        which doesn't make sense for websockets
        """
        pass

    def get_compression_options(self):
        # use deflate compress websocket
        return {}

    def authenticate(self):
        """Run before finishing the GET request

        Extend this method to add logic that should fire before
        the websocket finishes completing.
        """
        # authenticate the request before opening the websocket
        if self.get_current_user() is None:
            self.log.warning("Couldn't authenticate WebSocket connection")
            raise web.HTTPError(403)

        if self.get_argument('session_id', False):
            self.session.session = cast_unicode(self.get_argument('session_id'))
        else:
            self.log.warning("No session ID specified")

    def initialize(self):
        self.log.debug("Initializing websocket connection %s", self.request.path)
        self.session = Session(config=self.config)
        # TODO: make kernel client class configurable
        self.client = KernelGatewayWSClient()

    @gen.coroutine
    def get(self, kernel_id, *args, **kwargs):
        self.authenticate()
        self.kernel_id = cast_unicode(kernel_id, 'ascii')
        super(WebSocketChannelsHandler, self).get(kernel_id=kernel_id, *args, **kwargs)

    def open(self, kernel_id, *args, **kwargs):
        '''Handle web socket connection open to notebook server.'''
        # Delegate to web socket handler
        self.client.on_open(
            kernel_id=kernel_id,
            message_callback=self.write_message,
            compression_options=self.get_compression_options()
        )

    def on_message(self, message):
        '''Forward message to web socket handler.'''
        self.client.on_message(message)

    def write_message(self, message):
        '''Send message back to client.'''
        super(WebSocketChannelsHandler, self).write_message(message)

    def on_close(self):
        self.log.debug("Closing websocket connection %s", self.request.path)
        self.client.on_close()
        super(WebSocketChannelsHandler, self).on_close()

class KernelGatewayWSClient(LoggingConfigurable):
    '''Proxy web socket connection to a kernel gateway.'''

    def __init__(self):
        self.ws = None
        self.ws_future = Future()

    @gen.coroutine
    def _connect(self, kernel_id):
        ws_url = url_path_join(
            KG_URL.replace('http', 'ws'), 
            '/api/kernels', 
            url_escape(kernel_id),
            'channels'
        )
        self.log.info('Connecting to {}'.format(ws_url))
        request = HTTPRequest(ws_url, headers=KG_HEADERS)
        self.ws_future = websocket_connect(request)
        self.ws = yield self.ws_future
        # TODO: handle connection errors/timeout

    def _disconnect(self):
        if self.ws is not None:
            # Close connection
            self.ws.close()
        elif not self.ws_future.done():
            # Cancel pending connection
            self.ws_future.cancel()

    @gen.coroutine
    def _read_messages(self, callback):
        '''Read messages from server.'''
        while True:
            message = yield self.ws.read_message()
            if message is None: break # TODO: handle socket close
            callback(message)

    def on_open(self, kernel_id, message_callback, **kwargs):
        '''Web socket connection open.'''
        self._connect(kernel_id)
        loop = IOLoop.current()
        loop.add_future(
            self.ws_future,
            lambda future: self._read_messages(message_callback)
        )

    def on_message(self, message):
        '''Send message to server.'''
        if self.ws is None:
            loop = IOLoop.current()
            loop.add_future(
                self.ws_future,
                lambda future: self._write_message(message)
            )
        else:
            self._write_message(message)

    def _write_message(self, message):
        '''Send message to server.'''
        self.ws.write_message(message)

    def on_close(self):
        '''Web socket closed event.'''
        self._disconnect()

#-----------------------------------------------------------------------------
# kernel handlers
#-----------------------------------------------------------------------------

class MainKernelHandler(APIHandler):
    """Replace default MainKernelHandler to enable async lookup of kernels."""

    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self):
        km = self.kernel_manager
        kernels = yield gen.maybe_future(km.list_kernels())
        self.finish(json.dumps(kernels))

    @web.authenticated
    @json_errors
    @gen.coroutine
    def post(self):
        km = self.kernel_manager
        model = self.get_json_body()
        if model is None:
            model = {
                'name': km.default_kernel_name
            }
        else:
            model.setdefault('name', km.default_kernel_name)

        kernel_id = yield gen.maybe_future(km.start_kernel(kernel_name=model['name']))
        # This is now an async operation
        model = yield gen.maybe_future(km.kernel_model(kernel_id))
        location = url_path_join(self.base_url, 'api', 'kernels', url_escape(kernel_id))
        self.set_header('Location', location)
        self.set_status(201)
        self.finish(json.dumps(model))

class KernelHandler(APIHandler):
    """Replace default KernelHandler to enable async lookup of kernels."""

    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self, kernel_id):
        km = self.kernel_manager
        # This is now an async operation
        model = yield gen.maybe_future(km.kernel_model(kernel_id))
        if model is None:
            raise web.HTTPError(404, u'Kernel does not exist: %s' % kernel_id)
        self.finish(json.dumps(model))

    @web.authenticated
    @json_errors
    @gen.coroutine
    def delete(self, kernel_id):
        km = self.kernel_manager
        yield gen.maybe_future(km.shutdown_kernel(kernel_id))
        self.set_status(204)
        self.finish()

class KernelActionHandler(APIHandler):
    """Replace default KernelActionHandler to enable async lookup of kernels."""

    @web.authenticated
    @json_errors
    @gen.coroutine
    def post(self, kernel_id, action):
        km = self.kernel_manager
        if action == 'interrupt':
            km.interrupt_kernel(kernel_id)
            self.set_status(204)
        if action == 'restart':

            try:
                yield gen.maybe_future(km.restart_kernel(kernel_id))
            except Exception as e:
                self.log.error("Exception restarting kernel", exc_info=True)
                self.set_status(500)
            else:
                # This is now an async operation
                model = yield gen.maybe_future(km.kernel_model(kernel_id))
                self.write(json.dumps(model))
        self.finish()

#-----------------------------------------------------------------------------
# kernel spec handlers
#-----------------------------------------------------------------------------

class MainKernelSpecHandler(APIHandler):
    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self):
        ksm = self.kernel_spec_manager
        kernel_specs = yield gen.maybe_future(ksm.list_kernel_specs())
        # TODO: Remove resources until we support them
        for name, spec in kernel_specs['kernelspecs'].items():
            spec['resources'] = {}
        self.set_header("Content-Type", 'application/json')
        self.finish(json.dumps(kernel_specs))

class KernelSpecHandler(APIHandler):
    @web.authenticated
    @json_errors
    @gen.coroutine
    def get(self, kernel_name):
        ksm = self.kernel_spec_manager
        kernel_spec = yield ksm.get_kernel_spec(kernel_name)
        if kernel_spec is None:
            raise web.HTTPError(404, u'Kernel spec %s not found' % kernel_name)
        # TODO: Remove resources until we support them
        kernel_spec['resources'] = {}
        self.set_header("Content-Type", 'application/json')
        self.finish(json.dumps(kernel_spec))

#-----------------------------------------------------------------------------
# URL to handler mappings
#-----------------------------------------------------------------------------

from notebook.services.kernels.handlers import _kernel_id_regex, _kernel_action_regex
from notebook.services.kernelspecs.handlers import kernel_name_regex

default_handlers = [
    (r"/api/kernels", MainKernelHandler),
    (r"/api/kernels/%s" % _kernel_id_regex, KernelHandler),
    (r"/api/kernels/%s/%s" % (_kernel_id_regex, _kernel_action_regex), KernelActionHandler),
    (r"/api/kernels/%s/channels" % _kernel_id_regex, WebSocketChannelsHandler),
    (r"/api/kernelspecs", MainKernelSpecHandler),
    (r"/api/kernelspecs/%s" % kernel_name_regex, KernelSpecHandler),
    # TODO: support kernel spec resources
    # (r"/kernelspecs/%s/(?P<path>.*)" % kernel_name_regex, KernelSpecResourceHandler),
]
