# 分布式地处理-PyWPS-PyQGIS服务镜像

一个集成了许多开源算子的服务镜像，包含下列开源算子：

- QGIS，包括GDAL和GRASS
- OTB
- SAGA

所有算子都加载到了QGIS中，并通过PyQGIS调用，通过PyWPS发布为符合WPS 2.0规范的服务，该镜像基于[开源GIS算子环境](https://hub.docker.com/r/swsk33/op-gis-environment)构建。

# 说明

## 1，创建并运行容器

使用以下命令创建容器：

```bash
docker run -id --name pyqgis-wps -p 5000:5000 \
	-v pywps-data:/workdir \
	swsk33/distribute-geoprocessing-pywps-pyqgis
```

通过该命令，我们创建了容器，并暴露了`5000`端口，挂载数据卷`pywps-data`作为配置和数据数据卷。

## 2，修改配置文件

上述已经创建了容器，不过由于配置文件还未配置，因此无法正常运行，因此还需要修改数据卷中的`pywps.cfg`文件，需要修改的配置如下：

```properties
[MongoDB]
host = 127.0.0.1
port = 27017
db_name = pywps
username = daguo
password = 123456

[Redis]
host = 127.0.0.1
port = 6379
db = 0
password = 123456

[consul]
consul_ip = 202.114.148.161
consul_port = 8500
service_name = py-wps
service_ip = 127.0.0.1
service_port = 5000

[file]
file_server_url = http://127.0.0.1:9000/api/file

[deploy]
mode = single
;mode = distributed
```

- `[MongoDB]`部分需要配置一个可用的MongoDB数据库地址、端口和认证信息，用于持久化算子元数据
- `[Redis]`部分需要配置一个可用的Redis数据库地址、端口和认证信息，用于分布式异步计算时缓存进程信息
- `[consul]`部分需要配置Consul的地址和端口、服务名称、WPS服务的外网可访问地址和端口，用于服务注册和服务发现
- `[file]`部分需要配置WPS服务的文件服务地址，通常是网关的地址，文件服务的API路径，对于网关请参阅[分布式地处理-网关](https://hub.docker.com/r/swsk33/distribute-geoprocessing-gateway)镜像，对于文件服务请参阅[分布式地处理-文件服务](https://hub.docker.com/r/swsk33/distribute-geoprocessing-file)镜像
- `[deploy]`部分可配置该节点是以单机节点还是集群分布式模式运行

正确配置完成后，通过`docker restart`重启容器即可。