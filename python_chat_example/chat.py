# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import argparse
import sys
import threading
import queue
from tornado.escape import json_encode, json_decode, url_escape
from tornado.websocket import websocket_connect
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from uuid import uuid4
import asyncio

async def connect(address, kernel_id):
    base_url = 'http://' + address
    base_ws_url = 'ws://' + address

    client = AsyncHTTPClient()
    if not kernel_id:
        response = await client.fetch(
            '{}/api/kernels'.format(base_url),
            method='POST',
            auth_username='fakeuser',
            auth_password='fakepass',
            body=json_encode({'name' : 'python'})
        )
        kernel = json_decode(response.body)
        kernel_id = kernel['id']

    ws_req = HTTPRequest(url='{}/api/kernels/{}/channels'.format(
            base_ws_url,
            url_escape(kernel_id)
        ),
        auth_username='fakeuser',
        auth_password='fakepass'
    )
    ws = await websocket_connect(ws_req)
    return ws, kernel_id

async def execute(code, ws, must_return_stream):
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
            'code': code,
            'silent': False,
            'store_history': False,
            'user_expressions' : {},
            'allow_stdin' : False
        },
        'metadata': {},
        'buffers': {}
    }))

    # Receive messages
    while True:
        msg = await ws.read_message()
        msg = json_decode(msg)
        msg_type = msg['msg_type']
        if msg_type == 'error':
            print('ERROR')
            print(msg)
            return
        parent_msg_id = msg['parent_header']['msg_id']
        if True:  # parent_msg_id == msg_id:
            if msg_type == 'stream':
                return msg['content']['text']
            if not must_return_stream:
                return

async def receive(ws):
    await execute("message = ''", ws, False)
    while True:
        await asyncio.sleep(0.2)
        message = await execute("print(message); message = ''", ws, True)
        if message is not None:
            if message.endswith('\n'):
                message = message[:-1]
            if message:
                print(message)

def add_input(input_queue):
    while True:
        input_queue.put(input())

async def send(ws):
    input_queue = queue.Queue()
    input_thread = threading.Thread(target=add_input, args=(input_queue,))
    input_thread.start()
    while True:
        await asyncio.sleep(0.2)
        if not input_queue.empty():
            text = input_queue.get()
            text = text.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"').replace("'", "\\'")
            await execute("message = '" + text + "'", ws, False)

async def main(rcv_address, snd_address, rcv_kernel_id, snd_kernel_id):
    if rcv_kernel_id is None:  # or snd_kernel_id is None
        new_kernels = True
    else:
        new_kernels = False
    rcv_ws, rcv_kernel_id = await connect(rcv_address, rcv_kernel_id)
    snd_ws, snd_kernel_id = await connect(snd_address, snd_kernel_id)
    if new_kernels:
        print('Launch in the remote terminal:')
        print(f'python {__file__} --local-address {snd_address} --remote-address {rcv_address} --local-kernel {snd_kernel_id} --remote-kernel {rcv_kernel_id}')
    await asyncio.gather(receive(rcv_ws), send(snd_ws))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Peer-to-peer chat.')
    parser.add_argument('--local-address', dest='rcv_address', default='127.0.0.1:8888',
                       help='local address (default: 127.0.0.1:8888)')
    parser.add_argument('--remote-address', dest='snd_address', default='127.0.0.1:8889',
                       help='remote address (default: 127.0.0.1:8889)')
    parser.add_argument('--local-kernel', dest='rcv_kernel_id', default=None,
                       help='local kernel id (default: None)')
    parser.add_argument('--remote-kernel', dest='snd_kernel_id', default=None,
                       help='remote kernel id (default: None)')
    args = parser.parse_args()
    asyncio.run(main(args.rcv_address, args.snd_address, args.rcv_kernel_id, args.snd_kernel_id))
