FROM jupyter/datascience-notebook

# Install Kernel Gateway
RUN pip install git+https://github.com/jupyter-incubator/kernel_gateway
#RUN pip install git+https://github.com/poplav/kernel_gateway.git@gateway_test_r

# Configure container startup
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway"]

CMD [ \
        "--KernelGatewayApp.api=notebook-http", \
        "--KernelGatewayApp.seed_uri=/srv/notebooks/scotch_api_r.ipynb", \
        "--KernelGatewayApp.ip=0.0.0.0" \
    ]

ADD notebooks/scotch_api_r.ipynb /srv/notebooks/