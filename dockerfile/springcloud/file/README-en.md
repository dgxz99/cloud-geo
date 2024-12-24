# CloudGeo - File Service

Service for hosting files during [CloudGeoPy](https://hub.docker.com/r/swsk33/cloud-geo-py) calls and runs, Distributed File Service is based on the MinIO API.

# Description

The image needs to be properly configured to connect to the MinIO Distributed File Service and the Consul Registry, which can be specified via environment variables:

|   variable name    |          description           |  type   |   default   |
| :----------------: | :----------------------------: | :-----: | :---------: |
|   `CONSUL_HOST`    |    Consul Registry Address     | String  | `127.0.0.1` |
|   `CONSUL_PORT`    |  Consul Registry Port Number   | Integer |   `8500`    |
|    `MINIO_HOST`    |         MinIO address          | string  | `127.0.0.1` |
|    `MINIO_PORT`    |       MinIO port number        | integer |   `9000`    |
| `MINIO_ACCESS_KEY` |    MinIO access secret key     | string  |   `null`    |
| `MINIO_SECRET_KEY` |  MinIO Encryption Secret Key   | string  |   `null`    |
|   `MINIO_BUCKET`   | MinIO storage file bucket name | string  | `wps-file`  |

The following is a sample command to create the container:

```bash
docker run -id --name cloud-geo-file-service -p 8800:8800 \
	-e CONSUL_HOST=example.consul.com \
	-e MINIO_HOST=example.minio.com \
	-e MINIO_ACCESS_KEY=example_access_key \
	-e MINIO_SECRET_KEY=example_secret_key \ 
	swsk33/cloud-geo-file
```

At this point the server is up and running on port `8800` and can be accessed directly.
