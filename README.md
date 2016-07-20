# Kernel Gateway Demos

Example applications of the [Jupyter Kernel Gateway](https://github.com/jupyter/kernel_gateway).

Contents:

|Folder|Summary|Kernel Gateway Mode|
|------|-------|-------------------|
|[cf_demo](cf_demo)|Recipe for deploying the scotch_demo microservice to [Cloud Foundry](https://www.cloudfoundry.org/) using the [Python buildpack](https://github.com/cloudfoundry/python-buildpack)|[notebook-http](http://jupyter-kernel-gateway.readthedocs.io/en/stable/http-mode.html)|
|[all_spark_kernels](docker-stacks/all-spark-kernels)|Repurposes the [jupyter/all-spark-notebook](https://github.com/jupyter/docker-stacks/tree/master/all-spark-notebook) Docker image to run a kernel gateway server instead of Jupyter Notebook server|[notebook-http](http://jupyter-kernel-gateway.readthedocs.io/en/stable/http-mode.html)|
|[microservice_demo](microservice_demo)|Example of using a notebook microservice as part of an IFTTT flow, http://blog.ibmjstart.net/2016/01/28/powering-your-application-with-a-notebook-microservice/|[notebook-http](http://jupyter-kernel-gateway.readthedocs.io/en/stable/http-mode.html)|
|[nb2kg](nb2kg)|Extension that makes Jupyter Notebook work with remote kernels provided by a kernel gateway server, http://blog.ibmjstart.net/2016/06/24/using-remote-kernels-jupyter-notebook-server/|[jupyter-websocket](http://jupyter-kernel-gateway.readthedocs.io/en/stable/websocket-mode.html)|
|[node_client_example](node_client_example)|Shows how to spawn kernels and evaluate code on them using a Node client based on [jupyter-js-services](https://github.com/jupyter/jupyter-js-services)|[jupyter-websocket](http://jupyter-kernel-gateway.readthedocs.io/en/stable/websocket-mode.html)|
|[python_client_example](python_client_example)|Shows how to spawn kernels and evaluate code on them using a Python client|[jupyter-websocket](http://jupyter-kernel-gateway.readthedocs.io/en/stable/websocket-mode.html)|
|[scotch_demo](scotch_demo)|Example of a notebook for scotch recommendations turned into a RESTful microservice, with three separate implementations in R, Julia, and Python|[notebook-http](http://jupyter-kernel-gateway.readthedocs.io/en/stable/http-mode.html)|
|[swagger-notebook-service](swagger-notebook-service)|Example of generating a notebook microservice template from a swagger spec and deploying it as a microservice, http://blog.ibmjstart.net/2016/01/28/notebook-microservice-and-swagger/|[notebook-http](http://jupyter-kernel-gateway.readthedocs.io/en/stable/http-mode.html)|

