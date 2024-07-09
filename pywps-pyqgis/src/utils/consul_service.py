import configparser
import os
from consul import Consul
from context.config import get_config_file_path

config_path = get_config_file_path()
config = configparser.ConfigParser()
config.read(config_path)

# Consul地址和端口
consul_host = config.get("consul", "consul_ip")
consul_port = config.getint("consul", "consul_port")

# 全局唯一Consul客户端对象
consul_client = Consul(host=consul_host, port=consul_port)


# 注册服务
def register_consul(service_name, service_address, service_port):
	# 服务ID，每个节点应该唯一
	service_id = f'{service_name}-{service_address}-{service_port}'
	# 注册服务
	consul_client.agent.service.register(
		service_id=service_id,
		name=service_name,
		address=service_address,
		port=service_port,
		tags=['dev'],
		check={
			'http': f'http://{service_address}:{service_port}/health',
			'interval': '10s',
			'timeout': '1s',
		})


# 注销节点
def deregister_consul(service_name, service_address, service_port):
	service_id = f'{service_name}-{service_address}-{service_port}'
	consul_client.agent.service.deregister(service_id)