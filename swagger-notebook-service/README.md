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

This service can be accessed from the [swagger editor](http://editor.swagger.io).
To get the editor to correctly interact with the API:
* Copy the contents of `SwaggerPetstoreSpec.yaml`
```
cat swagger-petstore-service/SwaggerPetstoreSpec.yaml | pbcopy
```
* Go to http://editor.swagger.io and paste the contents into the editor
* Modify the `host` property in the document to point to the `ip:port` of your docker container
