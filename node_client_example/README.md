# Example: NodeJS Client

Demonstrates a NodeJS client using jupyter-js-services sending Python or Scala code to a kernel gateway, through an nginx proxy, with basic auth configured. The code examples use the Spark API. 

**Note** that nginx only exists here to show that the kernel gateway can run behind a common proxy. (You can connect the client directly to the kernel gateway of course!)

```
git clone https://github.com/jupyter/kernel_gateway_demos
cd kernel_gateway_demos/node_client_example
docker-compose build
docker-compose up
```

When you run docker-compose up the first time, it will launch an nginx proxy, a kernel gateway, and the client  with all logs aggregated. The client will send the `src/example.py` code to the kernel gateway for execution. Once the client completes, it will exit. If you want to run the client again without restarting the other two services, do this in another terminal:

```
docker-compose run -e DEMO_LANG=<scala|python|r> client
```

You can also run the `src/client.js` on your host without Docker if you `npm install` its dependencies and configure it with the proper environment variables. See what the `docker-compose.yml` and `Dockerfile.client` do as a reference.
