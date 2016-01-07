# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/datascience-notebook
MAINTAINER Jupyter Project <jupyter@googlegroups.com>

# Install Kernel Gateway
RUN pip install jupyter-kernel-gateway

# Configure container startup
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway", "--KernelGatewayApp.api=notebook-http", "--KernelGatewayApp.ip=0.0.0.0", "--KernelGatewayApp.seed_uri=/srv/notebooks/meetup_service.ipynb"]

# Add notebook served by the kernel gateway
ADD meetup_service.ipynb /srv/notebooks/

# Run container as user jovyan
USER jovyan
