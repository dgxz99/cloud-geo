# 分布式地处理-文件服务

用于[分布式地处理算子](https://hub.docker.com/r/swsk33/distribute-geoprocessing-pywps-pyqgis)调用和运行过程中，托管文件的服务，分布式文件服务基于MinIO API。

# 说明

该镜像需要正确指定一些配置使得其能够连接至MinIO分布式文件服务和Consul注册中心，可通过环境变量指定相关配置：

|       变量名       |         描述         |  类型  |   默认值    |
| :----------------: | :------------------: | :----: | :---------: |
|   `CONSUL_HOST`    |  Consul注册中心地址  | 字符串 | `127.0.0.1` |
|   `CONSUL_PORT`    | Consul注册中心端口号 |  整型  |   `8500`    |
|    `MINIO_HOST`    |      MinIO地址       | 字符串 | `127.0.0.1` |
|    `MINIO_PORT`    |     MinIO端口号      |  整型  |   `9000`    |
| `MINIO_ACCESS_KEY` |    MinIO访问秘钥     | 字符串 |   `null`    |
| `MINIO_SECRET_KEY` |    MinIO加密秘钥     | 字符串 |   `null`    |
|   `MINIO_BUCKET`   | MinIO存放文件桶名称  | 字符串 | `wps-file`  |

以下是一个示例命令，创建容器：

```bash
docker run -id --name wps-file-service -p 8800:8800 \
	-e CONSUL_HOST=example.consul.com \
	-e MINIO_HOST=example.minio.com \
	-e MINIO_ACCESS_KEY=example_access_key \
	-e MINIO_SECRET_KEY=example_secret_key \
	swsk33/distribute-geoprocessing-file
```

此时服务端已经启动，端口为`8800`，可直接访问。
