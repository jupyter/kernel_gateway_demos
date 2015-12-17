# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: help build dev

IMAGE=jupyterincubator/kernel_gateway_demos_port

help:
	@echo 'Host commands:'
	@echo 'build - builds the container image'
	@echo 'dev - starts running container (use on local machine)'

build:
	@docker build -no-cache -t $(IMAGE) .

dev:
	@docker run --rm -ti -p 8888:8888 $(IMAGE)
