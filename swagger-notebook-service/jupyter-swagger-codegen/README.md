# Swagger Codegen for Jupyter Notebooks

##Overview
This project is a Swagger module for generating Jupyter notebooks to implement 
REST APIs. This is achieved by generating a Jupyter notebook with cells 
compatible with the [Jupyter Kernel Gateway extension](https://github.com/jupyter-incubator/kernel_gateway).

##Usage

Make sure you have [docker](https://www.docker.com/) and Make installed. 
From there you simply need to invoke the make targets to generate the notebook.

```
make gen
```

This will generate notebooks under `target/swagger/{KERNEL}/src/`. 

The pet store swagger spec is used by default. If you have a local swagger.json, 
simply add it to the project and invoke the make target with 
`SWAGGER_SPEC=/src/{your_file}`. A remote swagger json can be specified in a
 similar fashion.


By default the notebook is generated against the _python3_ kernel. An 
alternative kernel can be specified by adding the `KERNEL` environment variable.
See the Supported Kernels section below for available kernels, or the Extending
section to add your own.

##Supported Kernels

* Python 3 - python3
* Python 2 - python2
* Spark Kernel - spark

##Extending

Adding support for your own interpreter is fairly straight forward. Look at the 
documentation in `IKernelInfo.java` to understand the values you need to supply.
When you have implemented `IKernelInfo` for your interpreter, say 
`my.own.Interpreter`, you will need to add the fully qualified name to
`src/main/resources/META-inf.services/org.jupyter.server.kernels.IKernelInfo`.
