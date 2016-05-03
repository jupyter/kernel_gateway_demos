## Advanced Python Client Example

The code in this example shows how to connect multiple clients to a kernel. To get started:

```
git clone https://github.com/jupyter/kernel_gateway_demos
cd kernel_gateway_demos/python_client_advanced_example
docker-compose build
docker-compose up
```

On startup there is a kernel and client created. When the kernels is created, the kernel id and a command to connect 
another client is printed. You should use this command in another terminal window. An example of this output is:

```
Created kernel KERNEL_ID. Connect other clients with the following command:
           docker-compose run client --kernel-id=KERNEL_ID
```

If you do not specify a `kernel-id` option a new one will be created. The options for the client are:

```
--code                           The code to execute on the kernel. (default
                                 print('hello, world!'))
--kernel-id                      The id of an existing kernel for connecting
                                 and executing code. If not specified, a new
                                 kernel will be created.
--lang                           The kernel language if a new kernel will be
                                 created. (default python)
--times                          The number of times to execute the code
                                 string. (default 2)
```
