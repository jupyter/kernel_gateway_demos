FROM jupyter/datascience-notebook:092fe70190dc

# Install latest stable Kernel Gateway
RUN pip install jupyter_kernel_gateway

# Configure container startup
ENTRYPOINT ["tini", "--", "jupyter", "kernelgateway", "--KernelGatewayApp.api=notebook-http", "--KernelGatewayApp.ip=0.0.0.0"]

# Add notebook apis used by the kernel gateway
ADD notebooks/scotch_api_r.ipynb /srv/notebooks/
ADD notebooks/scotch_api_julia.ipynb /srv/notebooks/
ADD notebooks/scotch_api_python.ipynb /srv/notebooks/
RUN chmod -R 555 /srv/notebooks

# Run container as user jovyan
USER jovyan

# Install additional packages used by notebook during build time
RUN julia -e 'Pkg.add("JSON")' && julia -e 'Pkg.add("Requests")'
