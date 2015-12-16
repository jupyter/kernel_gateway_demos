# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/all-spark-notebook:dbb9c7b50531

# Install Kernel Gateway
RUN pip install git+https://github.com/jupyter-incubator/kernel_gateway.git

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
