# 分布式地处理-地理处理（PyWPS-PyQGIS）服务镜像

一个集成了许多开源算子的服务镜像，包含下列开源算子：

- QGIS，包括GDAL和GRASS
- OTB
- SAGA

所有算子都加载到了QGIS中，并通过PyQGIS调用，通过PyWPS发布为符合WPS 2.0规范的服务，该镜像基于[开源GIS算子环境](https://hub.docker.com/r/swsk33/op-gis-environment)构建。
# 说明

该镜像需要正确指定一些相应配置使得其能够正常运行，可通过环境变量指定相关配置：

- **单节点部署：**DEPLOY_MODE为single，还需要设置MongoDB相关的配置。
- **分布式部署：**DEPLOY_MODE为distributed，MongoDB、Redis、Consul以及FILE_SERVER_URL这些都需要进行指定。

## 地理处理服务模块

|       变量名        |                      描述                       |  类型  |   默认值    |
| :-----------------: | :---------------------------------------------: | :----: | :---------: |
|     `WORK_DIR`      |     项目的工作目录（数据、配置文件、日志）      | 字符串 | `/workdir`  |
|    `MONGO_HOST`     |                MongoDB数据库地址                | 字符串 | `127.0.0.1` |
|    `MONGO_PORT`     |               MongoDB数据库端口号               |  整型  |   `27017`   |
|   `MONGO_DB_NAME`   |                MongoDB数据库名称                | 字符串 |   `pywps`   |
|  `MONGO_USERNAME`   |               MongoDB数据库用户名               | 字符串 |   `null`    |
|  `MONGO_PASSWORD`   |                MongoDB数据库密码                | 字符串 |   `null`    |
|    `REDIS_HOST`     |                 Redis数据库地址                 | 字符串 | `127.0.0.1` |
|    `REDIS_PORT`     |                 Redis数据库端口                 |  整型  |   `6379`    |
|     `REDIS_DB`      |                   Redis数据库                   |  整型  |     `0`     |
|  `REDIS_PASSWORD`   |                 Redis数据库密码                 | 字符串 |   `null`    |
|     `CONSUL_IP`     |               Consul注册中心地址                | 字符串 | `127.0.0.1` |
|    `CONSUL_PORT`    |              Consul注册中心端口号               |  整型  |   `8500`    |
|   `SERVICE_NAME`    |             注册到Consul的服务名称              | 字符串 |  `py-wps`   |
|    `SERVICE_IP`     |             注册到Consul的服务地址              | 字符串 |   `null`    |
|   `SERVICE_PORT`    |             注册到Consul的服务端口              |  整型  |   `5000`    |
|  `FILE_SERVER_URL`  | 文件服务URL，如：http://127.0.0.1:8000/api/file | 字符串 |   `null`    |
|    `DEPLOY_MODE`    |          部署模式：single与distributed          | 字符串 |  `single`   |
|  `UWSGI_PROCESSES`  |                   uWSGI进程数                   |  整型  |     `2`     |
|   `UWSGI_THREADS`   |              uWSGI线程数，最小为2               |  整型  |     `2`     |
| `UWSGI_BUFFER_SIZE` |            uWSGI缓冲区大小，字节单位            | 字符型 |   `32768`   |

注意：

- `SERVICE_IP`字段，即使本地也需要填写本地的IP地址，而不是`127.0.0.1`。docker容器部署，**同一网络**下填写容器名即可以。

以下是一个示例命令，创建容器：

```bash
# 单节点部署
docker run -id --name pywps-pyqgis \
        -p 5000:5000 \
        -v pywps-data:/workdir \
        -e MONGO_HOST=example.mongo.com \
        -e MONGO_USERNAME=example_username \
        -e MONGO_PASSWORD=example_password \
        swsk33/distribute-geoprocessing-pywps-pyqgis

# 分布式部署（consul与所有节点都在同一docker网络下，若不在，SERVICE_IP使用相应的IP地址）
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
        swsk33/distribute-geoprocessing-pywps-pyqgis
```

