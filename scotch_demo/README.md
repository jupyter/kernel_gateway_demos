# Kernel Gateway Language Support Demonstration

The [Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) is a
[JupyterApp](https://github.com/jupyter/jupyter_core/blob/master/jupyter_core/application.py) that
implements different APIs and protocols for accessing Jupyter kernels.  We can use the Jupyter kernel gateway to
[process requests](https://github.com/jupyter-incubator/kernel_gateway#processing-requests) and transform an
 annotated notebook into a HTTP API using the Jupyter kernel gateway.

The example notebooks show how one can use the Jupyter kernel gateway in a language agnostic manner by implementing a
[Scotch Api Notebook](https://github.com/jupyter-incubator/kernel_gateway/blob/master/etc/api_examples/scotch_api.ipynb)
in R, Julia, and Python:

* [R Scotch API](notebooks/scotch_api_r.ipynb)
* [Julia Scotch API](notebooks/scotch_api_julia.ipynb)
* [Python Scotch API](notebooks/scotch_api_python.ipynb)

### Build the docker container
```
make build
```

### Run the docker container for the scotch R api
```
make r_api
```

### Run the docker container for the scotch Julia api
```
make julia_api
```

### Run the docker container for the scotch Python api
```
make python_api
```

### Query the API:
To test the services point your web browser to:

* http://:8888/scotches - returns a JSON representation of all available scotches
* http://:8888/scotches/Ardbeg - returns a JSON representation of all the features of the queried scotch (Ardbeg)
* http://:8888/scotches/Ardbeg/similar - returns a JSON representation of the most similar scotches to the one requested
(Ardbeg)

<dl>
  <dt>Additional notes</dt>
  <dd>As the purpose of these notebooks is to demonstrate the multilanguage support of the kernel gateway,
  the API output may be slightly different between the various languages.</dd>
 </dl>
