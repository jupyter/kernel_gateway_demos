# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

.PHONY: config

SWAGGER_VERSION?=2.1.4
SWAGGER_SPEC?=http://petstore.swagger.io/v2/swagger.json
KERNEL?=python3
APP_VERSION?=1.0.0
REPO=maven:3.3.3-jdk-7

clean:
	@docker run -it --rm \
	 -v `pwd`:/src \
	 -v `pwd`/target/.m2:/root/.m2 \
	 -w /src \
	 $(REPO) mvn clean
	@rm swagger-codegen-cli-$(SWAGGER_VERSION).jar 2> /dev/null || true

swagger-codegen-cli-$(SWAGGER_VERSION).jar:
	@docker run -it --rm \
		 -v `pwd`:/src \
		 -v `pwd`/target/.m2:/root/.m2 \
		 -w /src \
		 $(REPO) curl http://repo1.maven.org/maven2/io/swagger/swagger-codegen-cli/${SWAGGER_VERSION}/swagger-codegen-cli-${SWAGGER_VERSION}.jar -o swagger-codegen-cli-${SWAGGER_VERSION}.jar

download_swagger: swagger-codegen-cli-$(SWAGGER_VERSION).jar

install: src
	@docker run -it --rm \
  	 -v `pwd`:/src \
  	 -v `pwd`/target/.m2:/root/.m2 \
  	 -w /src \
  	 $(REPO) mvn install -Dversion=$(APP_VERSION) -Dswagger-codegen-version=$(SWAGGER_VERSION)
	
config:
	@echo '{ "kernel" : "$(KERNEL)" }' > target/config.json
	
gen: install config download_swagger
	@docker run -it --rm \
			 -v `pwd`:/src \
			 -v `pwd`/target/.m2:/root/.m2 \
			 -w /src \
			 $(REPO) java -cp swagger-codegen-cli-${SWAGGER_VERSION}.jar:target/jupyter-swagger-codegen-$(APP_VERSION).jar \
               	io.swagger.codegen.Codegen -i ${SWAGGER_SPEC} -l jupyter -c target/config.json
