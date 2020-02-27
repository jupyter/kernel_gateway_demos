## Python peer-to-peer chat example

The code in this example shows how to create a simple peer-to-peer chat application.

Two kernels are created, one in the local machine and one in a remote machine. On the local machine, we connect to the local kernel as well as to the remote kernel, and we do the same on the other side. When you enter some text in the local machine, it will be assigned to a variable in the remote kernel. The remote kernel polls this variable and prints it on the remote machine. Of course implementing a chat system like this is overkill, but it is for educational purposes.

To get started:
```
conda create -n python_chat
conda activate python_chat
conda install -c conda-forge jupyter_kernel_gateway
jupyter kernelgateway --KernelGatewayApp.ip=127.0.0.1 --KernelGatewayApp.port=8888
```

In a new terminal (note the different port value):
```
conda activate python_chat
jupyter kernelgateway --KernelGatewayApp.ip=127.0.0.1 --KernelGatewayApp.port=8889
```

In a new terminal:
```
conda activate python_chat
git clone https://github.com/jupyter/kernel_gateway_demos
cd kernel_gateway_demos/python_chat_example
python chat.py --local-address 127.0.0.1:8888 --remote-address 127.0.0.1:8889
```

It will print instructions that you need to copy and paste in a new terminal, for instance (the kernel IDs will be different in your case):
```
conda activate python_chat
cd kernel_gateway_demos/python_chat_example
python chat.py --local-address 127.0.0.1:8889 --remote-address 127.0.0.1:8888 --local-kernel 74ba00f7-89c3-45af-89e7-fe35c7ce08fe --remote-kernel 43f99670-70d1-4e6e-bd07-307ca6c026ea
```

Now you can enter some text in one of the last two terminals, and it will be printed in the other one. Note that in the example above everything happens in the same machine, but it works over the Internet too!
