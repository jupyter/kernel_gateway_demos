FROM jupyter/datascience-notebook

# Install Kernel Gateway
RUN pip install git+https://github.com/jupyter-incubator/kernel_gateway
#RUN pip install git+https://github.com/poplav/kernel_gateway.git@gateway_test_r

# Configure container startup
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway", "--KernelGatewayApp.api=notebook-http", "--KernelGatewayApp.ip=0.0.0.0"]

ADD notebooks/scotch_api_r.ipynb /srv/notebooks/
ADD notebooks/scotch_api_julia.ipynb /srv/notebooks/