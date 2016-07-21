# Kernel Gateway Language Support Demonstration

The [Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) is a
[JupyterApp](https://github.com/jupyter/jupyter_core/blob/master/jupyter_core/application.py) that
implements different APIs and protocols for accessing Jupyter kernels.  We can use the Jupyter kernel gateway to
[process requests](https://github.com/jupyter-incubator/kernel_gateway#processing-requests) and transform an
 annotated notebook into a HTTP API using the Jupyter kernel gateway.

The example notebooks here show how one can use the Jupyter kernel gateway in a language agnostic manner by implementing a simple scotch recommendation API in R, Julia, and Python:

* [Python Scotch API](notebooks/scotch_api_python.ipynb)
* [R Scotch API](notebooks/scotch_api_r.ipynb)
* [Julia Scotch API](notebooks/scotch_api_julia.ipynb)

### Run the Examples

To run all three APIs, get docker and docker-compose. Then execute the following commands:

```
docker-compose build
docker-compose up
```

At this point, you'll have:

* The R API running on port 9000
* The Python API running on port 9001
* The Julia API running on port 9002
* A Jupyter Notebook server on port 8888 (so you can poke at the underlying notebooks)

The purpose of these notebooks is to demonstrate the multilanguage support of the kernel gateway. The API output may be slightly different between the various languages.

### Query the API

To test the services, point your web browser (or favorite web client) to one of the API ports above:

* http://127.0.0.1:PORT/scotches - returns a JSON representation of all available scotches
* http://127.0.0.1:PORT/scotches/Ardbeg - returns a JSON representation of all the features of the queried scotch (Ardbeg)
* http://127.0.0.1:PORT/scotches/Ardbeg/similar - returns a JSON representation of the most similar scotches to the one requested (Ardbeg)

### Updating the Notebooks

The docker-compose recipe here volume mounts the source notebooks into every container. If you make changes to one of the notebooks using the Jupyter Notebook server running on port 8888, the changes are not immediately reflected in the corresponding kernel gateway container until you restart it. For example, if you change the API defined in `scotch_api_python.ipynb`, you must run the following command to start using the new code in the Python API on port 9001:

```
docker-compose restart python_api
```
