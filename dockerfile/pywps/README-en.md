# Distributed Geoprocessing-Geoprocessing (PyWPS-PyQGIS) Service Mirror

A service mirror that integrates many open source operators and contains the following open source operators:

- QGIS, including GDAL and GRASS
- OTB
- SAGA

All operators are loaded into QGIS and invoked via PyQGIS and published as a WPS 2.0 compliant service via PyWPS, which is built on the [Open Source GIS Operator Environment](https://hub.docker.com/r/swsk33/op-gis-environment).

# Description

The image needs to be correctly specified some corresponding configuration to enable its normal operation, you can specify the relevant configuration through the environment variables:

- **Single node deployment:** DEPLOY_MODE is single, you also need to set the MongoDB related configuration.
- **Distributed deployment: **DEPLOY_MODE is distributed, MongoDB, Redis, Consul, and FILE_SERVER_URL need to be specified.

## Geoprocessing service module

|    Variable Name    |                      Description                       |   Type    |   Default   |
| :-----------------: | :----------------------------------------------------: | :-------: | :---------: |
|     `WORK_DIR`      | Project's working directory (data, config files, logs) |  string   | `/workdir`  |
|    `MONGO_HOST`     |                MongoDB database address                |  string   | `127.0.0.1` |
|    `MONGO_PORT`     |              MongoDB database port number              |  Integer  |   `27017`   |
|   `MONGO_DB_NAME`   |                 MongoDB database name                  |  string   |   `pywps`   |
|  `MONGO_USERNAME`   |               MongoDB database username                |  string   |   `null`    |
|  `MONGO_PASSWORD`   |               MongoDB database password                |  string   |   `null`    |
|    `REDIS_HOST`     |                 Redis database address                 |  string   | `127.0.0.1` |
|    `REDIS_PORT`     |                  Redis database port                   |  Integer  |   `6379`    |
|     `REDIS_DB`      |                     Redis database                     |  integer  |     `0`     |
|  `REDIS_PASSWORD`   |                Redis database password                 |  string   |   `null`    |
|     `CONSUL_IP`     |                Consul Registry Address                 |  string   | `127.0.0.1` |
|    `CONSUL_PORT`    |              Consul Registry Port Number               |  Integer  |   `8500`    |
|   `SERVICE_NAME`    |        Name of the service registered to Consul        |  string   |  `py-wps`   |
|    `SERVICE_IP`     |      Address of the service registered to Consul       |  string   |   `null`    |
|   `SERVICE_PORT`    |           Service port registered to Consul            |  Integer  |   `5000`    |
|  `FILE_SERVER_URL`  | File service URL, e.g. http://127.0.0.1:8000/api/file  |  string   |   `null`    |
|    `DEPLOY_MODE`    |        Deployment mode: single vs. distributed         |  string   |  `single`   |
|  `UWSGI_PROCESSES`  |                  uWSGI process count                   |  integer  |     `2`     |
|   `UWSGI_THREADS`   |           number of uWSGI threads, minimum 2           |  integer  |     `2`     |
| `UWSGI_BUFFER_SIZE` |               uWSGI buffer size in bytes               | Character |   `32768`   |

Notes:

- `SERVICE_IP` field, even if local you need to fill in the local IP address, not `127.0.0.1`. docker container deployment, **same network** under the fill in the container name can be.

Here is a sample command to create a container:

```bash
# Single node deployment
docker run -id --name pywps-pyqgis \
        -p 5000:5000 \
        -v pywps-data:/workdir \
        -e MONGO_HOST=example.mongo.com \
        -e MONGO_USERNAME=example_username \\
        -e MONGO_PASSWORD=example_password \
        swsk33/distribute-geoprocessing-pywps-pyqgis

# Distributed deployment (consul is under the same docker network as all nodes, if not, SERVICE_IP uses the appropriate IP address)
# node1
docker run -id \
        --name pywps-pyqgis-1 \
        -p 5001:5000 \
        -v pywps-data-1:/workdir \
        -e MONGO_HOST=example.mongo.com \
        -e MONGO_USERNAME=example_username \
        -e MONGO_PASSWORD=example_password \
        -e REDIS_HOST=example.redis.com \
        -e REDIS_PASSWORD=example_password \
        -e CONSUL_IP=consul \
        -e SERVICE_IP=pywps-pyqgis-1 \
        -e DEPLOY_MODE=distributed \
        -e FILE_SERVER_URL=http://wps-gateway:9000/api/file \
        --network pywps \
        swsk33/distribute-geoprocessing-pywps-pyqgis
# node2
docker run -id --name pywps-pyqgis-2 \
        -p 5002:5000 \
        -v pywps-data-2:/workdir \
        -e MONGO_HOST=example.mongo.com \
        -e MONGO_USERNAME=example_username \
        -e MONGO_PASSWORD=example_password \
        -e REDIS_HOST=example.redis.com \
        -e REDIS_PASSWORD=example_password \
        -e CONSUL_IP=example.consul.com \
        -e SERVICE_IP=pywps-pyqgis-2 \
        -e FILE_SERVER_URL=http://wps-gateway:9000/api/file \
        -e DEPLOY_MODE=distributed \
        --network pywps \
        swsk33/distributed-geoprocessing-pywps-pyqgis
```

