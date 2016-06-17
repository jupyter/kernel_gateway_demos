# Jupyter Notebook Extension to Kernel Gateway (nb2kg)

## Overview

**nb2kg** is a **demo** [Jupyter Notebook](https://github.com/jupyter/notebook) [server extension](http://jupyter-notebook.readthedocs.io/en/latest/extending/handlers.html#writing-a-notebook-server-extension)
that enables the Notebook server to use remote kernels hosted by a Jupyter [Kernel Gateway](https://github.com/jupyter/kernel_gateway).

The extension may be useful in cases where you want a local Notebook server to connect to a kernel that executes code on a compute cluster in the cloud, perhaps near big data (e.g., the kernel is a driver program running on an [Apache Spark](http://spark.apache.org/) cluster).

The extension overrides the `/api/kernels/*` and `/api/kernelspecs` request handlers of the Notebook server, and proxies all requests for these resources to a Kernel Gateway.  When you enable the extension, **all** kernels run on the configured Kernel Gateway instead of on the Notebook server host.

![Jupyter remote kernels](https://github.com/jupyter/kernel_gateway_demos/blob/master/nb2kg/deploy.png)

The **nb2kg** extension communicates with the Kernel Gateway using standard HTTP and web socket protocols.  This differs from other remote kernel projects, such as [remote_ikernel](https://pypi.python.org/pypi/remote_ikernel) and [rk](https://github.com/korniichuk/rk), which rely on SSH or other mechanisms to communicate with kernels.

The extension requires Jupyter Notebook 4.2 or later, with support for server extensions.

```
jupyter serverextension list
```

## Install

To install the **nb2kg** extension in an existing Notebook server environment:

```
pip install "git+https://github.com/jupyter/kernel_gateway_demos.git#egg=nb2kg&subdirectory=nb2kg"
jupyter serverextension enable --py nb2kg --sys-prefix
```

## Run Notebook server

When you run the Notebook server with the **nb2kg** extension enabled, you must set the `KG_URL` environment variable to the URL of the kernel gateway _and_ you must override the default kernel, kernel spec, and session managers:

```
export KG_URL=http://kg-host:port
jupyter notebook \
  --NotebookApp.session_manager_class=nb2kg.managers.SessionManager \
  --NotebookApp.kernel_manager_class=nb2kg.managers.RemoteKernelManager \
  --NotebookApp.kernel_spec_manager_class=nb2kg.managers.RemoteKernelSpecManager 
```

## Try It

You can use the included Dockerfiles to build and run a Notebook server with **nb2kg** enabled and a Kernel Gateway in separate Docker containers.

```
git clone https://github.com/jupyter/kernel_gateway_demos.git
cd kernel_gateway_demos/nb2kg
```

Build Notebook server and Kernel Gateway Docker images.

```
docker-compose build
```

Run the containers.

```
docker-compose up -d
```

Launch a web browser to the Notebook server.  On Mac OS X:

```
open http://my.docker.host:9888
```

## Develop

If you want to modify the extension, you can develop it within your Jupyter Notebook dev environment.

Clone this repo.

```
git clone https://github.com/jupyter/kernel_gateway_demos.git
cd kernel_gateway_demos/nb2kg
```

Install and enable the extension.

```
make install
```

Run the Jupyter Notebook server.

```
make dev
```

## Uninstall

To uninstall the **nb2kg** extension:

```
jupyter serverextension disable --py nb2kg --sys-prefix
pip uninstall -y nb2kg
```

## Caveats

* The extension is currently **demo** code.  YMMV.
* When you enable the extension, **all** kernels run on the configured Kernel Gateway, instead of on the Notebook server host.  The extension does not support local kernels.
* When you enable the extension, notebooks and other files reside on the Notebook server, which means that remote kernels may not have access to them.
* To move the extension beyond a demo would probably require changes to the [jupyter/notebook](https://github.com/jupyter/notebook) code base.  In particular,
	* The Notebook kernel API request handlers would need to support asynchronous operation for ALL kernel requests.  The extension currently must replace several manager and handler classes to add this support.
	* The Notebook server application could provide a hook to make it easier to override the default request handlers (e.g., `/api/kernels`).  [Tornado applications](http://www.tornadoweb.org/en/latest/web.html) pass requests to the first request handler registered for a particular URL path, and the Notebook registers default handlers before extension handlers.

