// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

var xmlhttprequest = require('xmlhttprequest');
var ws = require('ws');
var fs = require('fs');

global.XMLHttpRequest = xmlhttprequest.XMLHttpRequest;
global.WebSocket = ws;

var PYTHON_EXAMPLE = fs.readFileSync('example.py', {encoding: 'utf-8'});
var SCALA_EXAMPLE = fs.readFileSync('example.scala', {encoding: 'utf-8'});

var jupyter = require('jupyter-js-services');

var kg_host = process.env.GATEWAY_HOST || '192.168.99.100:8888';
var baseUrl = 'http://' + kg_host;
var demo_lang = process.env.DEMO_LANG === 'scala' ? 'scala' : 'python';
var demo_code = (demo_lang === 'scala') ? SCALA_EXAMPLE : PYTHON_EXAMPLE;

console.log('Targeting server:', kg_host);
console.log('Using demo lang:', demo_lang);

// extra headers to demo that it can be done
var ajaxSettings = {
    requestHeaders: {
        'X-Some-Header': 'some-value'
    }
};

// get info about the available kernels
jupyter.getKernelSpecs({ 
    baseUrl: baseUrl,
    ajaxSettings: ajaxSettings
}).then((kernelSpecs) => {
    console.log('Available kernelspecs:', kernelSpecs);

    // request a new kernel
    console.log('Starting kernel:', demo_lang)
    jupyter.startNewKernel({
        baseUrl: baseUrl,
        name: demo_lang,
        ajaxSettings: ajaxSettings
    }).then((kernel) => {
        // execute some code
        console.log('Executing sample code');
        var future = kernel.execute({ code: demo_code  } );
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
