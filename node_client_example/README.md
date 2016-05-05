# Example: NodeJS Client

Demonstrates a simple NodeJS client using jupyter-js-services sending Python or Scala code to a kernel gateway, through an nginx proxy. The code examples use the Spark API. The proxy only exists to show that the kernel gateway can run behind a common proxy.

```
git clone https://github.com/jupyter/kernel_gateway_demos
cd kernel_gateway_demos/node_client_example
docker-compose build
docker-compose up
```

When you run docker-compose up the first time, it will launch an nginx proxy, a kernel gateway, and the client running the `src/example.py` with all logs aggregated. Once the client completes, it will exist. If you want to run the client again without restarting the other two services, do this in another terminal:

```
docker-compose run -e DEMO_LANG=<scala|python|r> client
```

You can also run the node client right on your host if you configure it to point to the proxy like so:

```
cd kernel_gateway_demos/node_client_example
npm install
export GATEWAY_HOST=<ip of your docker host>:8080 
DEMO_LANG=<python|scala|r> node client.js
```
