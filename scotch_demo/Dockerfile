FROM jupyter/datascience-notebook:8015c88c4b11

# Install additional packages used by notebook during build time
RUN julia -e 'Pkg.add("JSON")' && julia -e 'Pkg.add("Requests")'

# Install latest stable Kernel Gateway
RUN pip install --no-cache-dir jupyter_kernel_gateway
