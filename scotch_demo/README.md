# Kernel Gateway Language Support Demonstration

The [Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) is a
[JupyterApp](https://github.com/jupyter/jupyter_core/blob/master/jupyter_core/application.py) that
implements different APIs and protocols for accessing Jupyter kernels.  We can use the Jupyter kernel gateway to
[process requests](https://github.com/jupyter-incubator/kernel_gateway#processing-requests) and transform an
 annotated notebook into a HTTP API using the Jupyter kernel gateway.

The example notebooks show how one can use the Jupyter kernel gateway in a language agnostic manner by implementing a
simple scotch recommendation API in R, Julia, and Python:

* [Python Scotch API](notebooks/scotch_api_python.ipynb)
* [R Scotch API](notebooks/scotch_api_r.ipynb)
* [Julia Scotch API](notebooks/scotch_api_julia.ipynb)

### Build the docker container
```
make build
```

### Run the docker container for the scotch R API
```
make r_api
```

### Run the docker container for the scotch Julia API
```
make julia_api
```

### Run the docker container for the scotch Python API
```
make python_api
```

### Query the API

To test the services point your web browser to the URLs exposed by the service on your Docker host:

* http://ip:8888/scotches - returns a JSON representation of all available scotches
* http://ip:8888/scotches/Ardbeg - returns a JSON representation of all the features of the queried scotch (Ardbeg)
* http://ip:8888/scotches/Ardbeg/similar - returns a JSON representation of the most similar scotches to the one requested
(Ardbeg)

As the purpose of these notebooks is to demonstrate the multilanguage support of the kernel gateway, the API output may be slightly different between the various languages.
