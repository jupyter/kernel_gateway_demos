# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
.PHONY: help build run

IMAGE=jupyterincubator/kernel_gateway_demos_microservice

help:
	@echo 'Host commands:'
	@echo 'build - builds the container image'
	@echo 'run   - starts running container of the meetup service API (use on local machine)'

build:
	@docker build --no-cache --rm -t $(IMAGE) .

run:
	@docker run --rm -it -p 8888:8888 -e ALCHEMY_KEY=$(ALCHEMY_KEY) -e MAKER_EVENT_NAME=$(MAKER_EVENT_NAME) -e MAKER_KEY=$(MAKER_KEY) $(IMAGE)
