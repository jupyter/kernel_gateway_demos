# Swagger to Notebook to Microservice

This sample project demonstrates how to use a [Swagger](http://swagger.io/) specification to generate a [Jupyter](http://jupyter.org/) notebook.
The generated notebook is then consumed by the [Jupyter Kernel Gateway](https://github.com/jupyter-incubator/kernel_gateway) and is turned into a REST microservice.

## Swagger Codegen Module
Located in `jupyter-swagger-codegen` a java project for generating notebooks from a swagger specification can be found. For information, see the README in that directory.

## Swagger Pet Store Implementation
There is a sample notebook, with supplemental files, in the `swagger-petstore-service` folder. This notebook can be packaged and run in a docker container:

```shell
cd swagger-petstore-service
# build the docker container
./package.sh

# run the docker container
./run.sh
```
