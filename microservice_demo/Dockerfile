FROM jupyter/pyspark-notebook:a388c4a66fd4
MAINTAINER Jupyter Project <jupyter@googlegroups.com>

RUN git clone https://github.com/jupyter-incubator/kernel_gateway.git && \
	cd kernel_gateway && \
	python setup.py install

ENV notebook=meetup_service.ipynb
COPY ${notebook} /home/$NB_USER/work/apinotebook.ipynb

