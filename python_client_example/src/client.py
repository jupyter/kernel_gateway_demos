# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from tornado import gen
from tornado.escape import json_encode, json_decode, url_escape
from tornado.websocket import websocket_connect
from tornado.ioloop import IOLoop
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import options, parse_command_line, define
from time import sleep
from uuid import uuid4

define("code", default="print('hello, world!')", help="The code to execute on the kernel.")
define("lang", default="python", help="The kernel language if a new kernel will be created.")
define("times", default=2, type=int, help="The number of times to execute the code string.")
define("kernel-id", default=None, help="The id of an existing kernel for connecting and executing code. If not specified, a new kernel will be created.")

@gen.coroutine
def main():
    # give other services a moment to come up in this example
    sleep(1)
    
    parse_command_line()
    
    base_url = os.getenv('BASE_GATEWAY_HTTP_URL', 'http://localhost:8888')
    base_ws_url = os.getenv('BASE_GATEWAY_WS_URL', 'ws://localhost:8888')
    
    print(base_url)
    print(base_ws_url)
    
    client = AsyncHTTPClient()
    kernel_id = options.kernel_id
    if not kernel_id:
        response = yield client.fetch(
            '{}/api/kernels'.format(base_url),
            method='POST',
            auth_username='fakeuser',
            auth_password='fakepass',
            body=json_encode({'name' : options.lang})
        )
        kernel = json_decode(response.body)
        kernel_id = kernel['id']
        print(
            '''Created kernel {0}. Connect other clients with the following command:
            docker-compose run client --kernel-id={0}
            '''.format(kernel_id)
        )
        
    ws_req = HTTPRequest(url='{}/api/kernels/{}/channels'.format(
            base_ws_url,
            url_escape(kernel_id)
        ),
        auth_username='fakeuser',
        auth_password='fakepass'
    )
    ws = yield websocket_connect(ws_req)
    print('Connected to kernel websocket')
    for x in range(0, options.times):
        print('Sending message {} of {}'.format(x+1, options.times))
        msg_id = uuid4().hex
        # Send an execute request
        ws.write_message(json_encode({
            'header': {
                'username': '',
                'version': '5.0',
                'session': '',
                'msg_id': msg_id,
                'msg_type': 'execute_request'
            },
            'parent_header': {},
            'channel': 'shell',
            'content': {
                'code': options.code,
                'silent': False,
                'store_history': False,
                'user_expressions' : {},
                'allow_stdin' : False
            },
            'metadata': {},
            'buffers': {}
        }))
        
        # Look for stream output for the print in the execute
        while 1:
            msg = yield ws.read_message()
            msg = json_decode(msg)
            msg_type = msg['msg_type']
            print('Received message type:', msg_type)
            if msg_type == 'error':
                print('ERROR')
                print(msg)
                break
            parent_msg_id = msg['parent_header']['msg_id']
            if msg_type == 'stream' and parent_msg_id == msg_id:
                print('  Content:', msg['content']['text'])
                break
            
    
    ws.close()

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
