# 分布式地处理-分布式网关

用于分布式地理处理服务的网关，实现服务负载均衡。

# 说明

通过以下命令创建容器：

```bash
docker run -id --name wps-gateway -p 9000:9000 \
	-e CONSUL_HOST=example.consul.com \
	-e CONSUL_PORT=8500 \
	swsk33/distribute-geoprocessing-gateway
```

需要正确配置Consul注册中心的地址和端口号。

此时服务端已经启动，端口为`9000`，可直接访问。
