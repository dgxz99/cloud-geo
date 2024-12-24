# CloudGeo - Distributed Gateway

Gateway for CloudGeo services to enable service load balancing.

# Description

Create the container with the following command:

```bash
docker run -id --name cloud-geo-gateway -p 9000:9000 \
	-e CONSUL_HOST=example.consul.com \
	-e CONSUL_PORT=8500 \
	swsk33/cloud-geo-gateway
```

The address and port number of the Consul registry needs to be configured correctly.

At this point the server is up and running on port `9000` and can be accessed directly.
