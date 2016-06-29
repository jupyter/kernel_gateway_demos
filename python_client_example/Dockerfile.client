# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM python:3.5.1-alpine

WORKDIR /src
RUN pip install tornado
COPY src/* /src/
ENTRYPOINT ["python", "/src/client.py"]
