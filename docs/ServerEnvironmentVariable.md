When the backend module is running, it supports the use of **environmental variables** to configure relevant configuration items for easy containerized deployment.

## 1, Gateway Module

| Variable Name | Description | Type | Default value |
| :-----------: | :------------------: | :----: | :---------: |
| `CONSUL_HOST` | Consul Registry Address | String | `127.0.0.1` |
| `CONSUL_PORT` | Consul Registry Port Number | Integer | `8500` |

## 2, File Service Module

| Variable Name | Description | Type | Default |
| :----------------: | :------------------: | :----: | :---------: |
| `CONSUL_HOST` | Consul Registry Address | String | `127.0.0.1` |
| `CONSUL_PORT` | Consul Registry Port Number | Integer | `8500` |
| `MINIO_HOST` | MinIO address | string | `127.0.0.1` |
| `MINIO_PORT` | MinIO port number | integer | `9000` |
| `MINIO_ACCESS_KEY` | MinIO access secret key | string | `null` |
| `MINIO_SECRET_KEY` | MinIO Encryption Secret Key | string | `null` |
| `MINIO_BUCKET` | MinIO storage file bucket name | string | `wps-file` |

- ## 3, Geoprocessing Service Module

	|    Variable Name    |                      Description                       |   Type    | Default Value |
	| :-----------------: | :----------------------------------------------------: | :-------: | :-----------: |
	| `SERVER_HOST` | Deployment IP address of the service | String | `127.0.0.1` |
	| `SERVER_PORT` | Deployment port of the service | Integer | `5000` |
	|     `WORK_DIR`      | Project's working directory (data, config files, logs) |  string   |  `/workdir`   |
	|    `MONGO_HOST`     |                MongoDB database address                |  string   |  `127.0.0.1`  |
	|    `MONGO_PORT`     |              MongoDB database port number              |  Integer  |    `27017`    |
	|   `MONGO_DB_NAME`   |                 MongoDB database name                  |  string   |    `pywps`    |
	|  `MONGO_USERNAME`   |               MongoDB database username                |  string   |    `null`     |
	|  `MONGO_PASSWORD`   |               MongoDB database password                |  string   |    `null`     |
	|    `REDIS_HOST`     |                 Redis database address                 |  string   |  `127.0.0.1`  |
	|    `REDIS_PORT`     |                  Redis database port                   |  Integer  |    `6379`     |
	|     `REDIS_DB`      |                     Redis database                     |  integer  |      `0`      |
	|  `REDIS_PASSWORD`   |                Redis database password                 |  string   |    `null`     |
	|     `CONSUL_IP`     |                Consul Registry Address                 |  string   |  `127.0.0.1`  |
	|    `CONSUL_PORT`    |              Consul Registry Port Number               |  Integer  |    `8500`     |
	|   `SERVICE_NAME`    |        Name of the service registered to Consul        |  string   |   `py-wps`    |
	|    `SERVICE_IP`     |      Address of the service registered to Consul       |  string   |    `null`     |
	|   `SERVICE_PORT`    |           Service port registered to Consul            |  Integer  |    `5000`     |
	|  `FILE_SERVER_URL`  | File service URL, e.g. http://127.0.0.1:8000/api/file  |  string   |    `null`     |
	|    `DEPLOY_MODE`    |        Deployment mode: single vs. distributed         |  string   |   `single`    |
	|  `UWSGI_PROCESSES`  |                  uWSGI process count                   |  integer  |      `2`      |
	|   `UWSGI_THREADS`   |           number of uWSGI threads, minimum 2           |  integer  |      `2`      |
	| `UWSGI_BUFFER_SIZE` |               uWSGI buffer size in bytes               | Character |    `32768`    |

	Notes:

	- For `SERVER_HOST` and `SERVER_PORT`, please fill in the ip and mapped port of the server when deploying the container.
	
	- `SERVICE_IP` field, even if local you need to fill in the local IP address, not `127.0.0.1`. docker container deployment, **same network** under the fill in the container name can be.
