# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM jupyter/all-spark-notebook:97a5071c5775

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

# Install Kernel Gateway
RUN pip install 'jupyter_kernel_gateway>=1.0,<2.0'

# Configure container startup, letting the user pass command line args through
# easily without disrupting the use of tini or the kernelgateway entry point
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway"]
CMD ["--KernelGatewayApp.ip=0.0.0.0"]
