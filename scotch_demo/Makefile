# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: help build r_api julia_api

IMAGE=jupyterincubator/kernel_gateway_demos_port

help:
	@echo 'Host commands:'
	@echo 'build - builds the container image'
	@echo 'r_api - starts running container of the scotch R api(use on local machine)'
	@echo 'julia_api - starts running container of the scotch Julia api(use on local machine)'
	@echo 'python_api - starts running container of the scotch Python api(use on local machine)'

build:
	@docker build -no-cache -t $(IMAGE) .

r_api:
	@docker run --rm -ti -p 8888:8888 $(IMAGE) --KernelGatewayApp.seed_uri=/srv/notebooks/scotch_api_r.ipynb

julia_api:
	@docker run --rm -ti -p 8888:8888 $(IMAGE) --KernelGatewayApp.seed_uri=/srv/notebooks/scotch_api_julia.ipynb

python_api:
	@docker run --rm -ti -p 8888:8888 $(IMAGE) --KernelGatewayApp.seed_uri=/srv/notebooks/scotch_api_python.ipynb
