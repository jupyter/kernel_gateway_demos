# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os

from notebook.utils import url_path_join
from .handlers import default_handlers as ext_handlers
from tornado.web import URLSpec

def _jupyter_server_extension_paths():
    '''API for server extension installation on notebook 4.2.'''
    return [{
        "module": "nb2kg"
    }]

def load_jupyter_server_extension(nb_app):
    '''Loads server extension.'''
    nb_app.log.info('Loaded nb2kg extension')
    # TODO: There is no clean way to override existing handlers that are already
    # registered with the Tornado application.  The first handler to match the
    # URL will handle the request, so we must prepend our handlers to override 
    # the existing ones.
    web_app = nb_app.web_app
    pattern, handlers = web_app.handlers[0]
    base_url = web_app.settings['base_url']
    for handler in ext_handlers[::-1]:
        pattern = url_path_join(base_url, handler[0])
        new_handler = URLSpec(pattern, *handler[1:])
        nb_app.log.info('Overriding handler %s' % new_handler)
        handlers.insert(0, new_handler)
