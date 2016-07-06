// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

var xmlhttprequest = require('xmlhttprequest');
var ws = require('ws');
var fs = require('fs');
global.XMLHttpRequest = xmlhttprequest.XMLHttpRequest;
global.WebSocket = ws;
var jupyter = require('jupyter-js-services');

var gatewayUrl = process.env.BASE_GATEWAY_HTTP_URL || 'http://localhost:8888';
var gatewayWsUrl = process.env.BASE_GATEWAY_WS_URL || 'ws://localhost:8888';

var demoLang = process.env.DEMO_LANG || 'python';
var demoInfo = {
    python: {
        kernelName: 'python',
        filename: 'example.py'
    },
    scala: {
        kernelName: 'scala',
        filename: 'example.scala'
    },
    r: {
        kernelName: 'ir',
        filename: 'example.r'
    }
}[demoLang];
var demoSrc = fs.readFileSync(demoInfo.filename, {encoding: 'utf-8'});

console.log('Targeting server:', gatewayUrl);
console.log('Using example code:', demoInfo.filename);

var ajaxSettings = {
    // Basic auth params are OK (hardcoding these for the demo nginx proxy)
    // but they only apply to the HTTP requests made by jupuyter-js-services
    // at the moment. https://github.com/jupyter/jupyter-js-services/issues/158
    user: 'fakeuser',
    password: 'fakepass',
    // extra headers are OK
    requestHeaders: {
        'X-Some-Header': 'some-value'
    }
};

// get info about the available kernels
jupyter.getKernelSpecs({ 
    baseUrl: gatewayUrl,
    ajaxSettings: ajaxSettings
}).then((kernelSpecs) => {
    console.log('Available kernelspecs:', kernelSpecs);

    // request a new kernel
    console.log('Starting kernel:', demoLang)
    jupyter.startNewKernel({
        baseUrl: gatewayUrl,
        wsUrl: gatewayWsUrl, // passing this separately to demonstrate basic auth
        name: demoInfo.kernelName,
        ajaxSettings: ajaxSettings
    }).then((kernel) => {
        // execute some code
        console.log('Executing sample code');
        var future = kernel.execute({ code: demoSrc } );
        future.onDone = () => {
            // quit the demo when done, but leave the kernel around
            process.exit(0);
        };
        future.onIOPub = (msg) => {
            // print received messages
            console.log('Received message:', msg);
        };
    }).catch(req => {
        console.log('Error starting new kernel:', req.xhr.statusText);
        process.exit(1);
    });
}).catch((req) => {
    console.log('Error fetching kernel specs:', req.xhr.statusText);
    process.exit(1);
});
