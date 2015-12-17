# Kernel Gateway Language Support Demonstration

The [Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) is a
[JupyterApp](https://github.com/jupyter/jupyter_core/blob/master/jupyter_core/application.py) that
implements different APIs and protocols for accessing Jupyter kernels.  We can use the Jupyter kernel gateway to
[process requests](https://github.com/jupyter-incubator/kernel_gateway#processing-requests) and transform an
 annotated notebook into a HTTP API using the Jupyter kernel gateway.

The example notebooks show how one can use the Jupyter kernel gateway in a language agnostic manner by porting the
[Scotch Api Notebook](https://github.com/jupyter-incubator/kernel_gateway/blob/master/etc/api_examples/scotch_api.ipynb)
from Python to R and Julia:

* [R Scotch API](https://github.com/jupyter-incubator/kernel_gateway_demos/scotch_demo/notebooks/scotch_api_r.ipynb)
* [Julia Scotch API](https://github.com/jupyter-incubator/kernel_gateway_demos/scotch_demo/notebooks/scotch_api_julia.ipynb)
