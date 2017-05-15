FROM jupyter/datascience-notebook:97a5071c5775

# Install additional packages used by notebook during build time
RUN julia -e 'Pkg.add("JSON")' && julia -e 'Pkg.add("Requests")'

# Install KG from master (for the static_path option)
RUN pip install 'git+https://github.com/jupyter/kernel_gateway'
