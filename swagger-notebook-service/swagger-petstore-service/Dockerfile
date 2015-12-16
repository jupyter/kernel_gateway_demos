FROM jupyter/all-spark-notebook:dbb9c7b50531

# Install Kernel Gateway
RUN pip install jupyter-kernel-gateway

# Configure container startup
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway"]

LABEL version="1.0.0"
LABEL service="Swagger Petstore"

CMD [ \
        "--KernelGatewayApp.api=notebook-http", \
        "--KernelGatewayApp.seed_uri=/srv/notebooks/SwaggerPetstoreApi.ipynb", \
        "--KernelGatewayApp.ip=0.0.0.0" \
    ]

ADD SwaggerPetstoreApi.ipynb /srv/notebooks/



