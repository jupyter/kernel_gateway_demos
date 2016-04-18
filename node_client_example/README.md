# Example: NodeJS Client

Demonstrates a simple NodeJS client using jupyter-js-services sending Python or Scala code to a kernel gateway, through an nginx proxy. The Python / Scala code examples use the Spark API.

```
# in one terminal
git clone https://github.com/jupyter/kernel_gateway_demos
cd kernel_gateway_demos/node_client_example
docker-compose build
docker-compose up

# in another
cd kernel_gateway_demos/node_client_example
npm install
export GATEWAY_HOST=<ip of your docker host>:8080 
DEMO_LANG=<python|scala> node client.js
```
