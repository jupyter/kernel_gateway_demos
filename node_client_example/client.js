var xmlhttprequest = require('xmlhttprequest');
var ws = require('ws');
var fs = require('fs');

global.XMLHttpRequest = xmlhttprequest.XMLHttpRequest;
global.WebSocket = ws;

var PYTHON_EXAMPLE = fs.readFileSync('example.py', {encoding: 'utf-8'});
var SCALA_EXAMPLE = fs.readFileSync('example.scala', {encoding: 'utf-8'});

var jupyter = require('jupyter-js-services');

var kg_host = process.env.GATEWAY_HOST || '192.168.99.100:8888';
var demo_lang = process.env.DEMO_LANG === 'scala' ? 'scala' : 'python';
var demo_code = (demo_lang === 'scala') ? SCALA_EXAMPLE : PYTHON_EXAMPLE;

console.log('Targeting server:', kg_host);
console.log('Using demo lang:', demo_lang);

// get info about the available kernels and start a new one
jupyter.getKernelSpecs('http://'+kg_host).then((kernelSpecs) => {
    console.log('Available kernelspecs:', kernelSpecs);
    var options = {
        baseUrl: 'http://'+kg_host,
        wsUrl: 'ws://'+kg_host,
        name: demo_lang
    };
    // request a kernel in the default language (python)
    console.log('Starting kernel:', demo_lang)
    jupyter.startNewKernel(options).then((kernel) => {
        // execute some code
        console.log('Executing sample code');
        var future = kernel.execute({ code: demo_code  } );
        future.onDone = () => {
            // quit when done
            process.exit(0);
        };
        future.onIOPub = (msg) => {
            // print received messages
            console.log('Received message:', msg);
        };
    });
});
