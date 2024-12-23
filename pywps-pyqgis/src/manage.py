import argparse
import os

from config import get_config

parser = argparse.ArgumentParser(description='Run Flask app with specific configuration.')

# 服务ip与端口
parser.add_argument('--server_host', default='127.0.0.1', help='Host IP address')
parser.add_argument('--server_port', type=int, default=5000, help='Server Port')

# MongoDB配置
parser.add_argument('--mongo_host', default='127.0.0.1', help='MongoDB host')
parser.add_argument('--mongo_port', type=int, default=27017, help='MongoDB port')
parser.add_argument('--mongo_db_name', default='pywps', help='MongoDB database name')
parser.add_argument('--mongo_username', default='', help='MongoDB username')
parser.add_argument('--mongo_password', default='', help='MongoDB password')

# Redis配置
parser.add_argument('--redis_host', default='127.0.0.1', help='Redis host')
parser.add_argument('--redis_port', type=int, default=6379, help='Redis port')
parser.add_argument('--redis_db', type=int, default=0, help='Redis database number')
parser.add_argument('--redis_password', default='123456', help='Redis password')

# Consul配置
parser.add_argument('--consul_ip', default='127.0.0.1', help='Consul IP address')
parser.add_argument('--consul_port', type=int, default=8500, help='Consul port')
parser.add_argument('--consul_service_name', default='py-wps', help='Service name')
parser.add_argument('--consul_service_ip', default='', help='Consul Service IP address')
parser.add_argument('--consul_service_port', type=int, default=5000, help='Consul Service port')

# 文件服务配置
parser.add_argument('--file_server_url', default='http://127.0.0.1:8000/api/file', help='File server URL')

# 部署模式
parser.add_argument('--deploy_mode', choices=['single', 'distributed'], default='single', help='Deployment mode (e.g., single, distributed)')

# 工作目录
parser.add_argument('--work_dir', help='Working directory for the application', default=os.path.dirname(os.path.dirname(__file__)))

args = parser.parse_args()
# 切换工作目录
if args.work_dir is not None:
	os.chdir(args.work_dir)

# 使用字典更新覆盖配置
config_updates = {
	'Server': {
		'server_host': args.server_host,
		'server_port': args.server_port,
	},
	'MongoDB': {
		'host': args.mongo_host,
		'port': args.mongo_port,
		'db_name': args.mongo_db_name,
		'username': args.mongo_username,
		'password': args.mongo_password,
	},
	'Redis': {
		'host': args.redis_host,
		'port': args.redis_port,
		'db': args.redis_db,
		'password': args.redis_password,
	},
	'consul': {
		'consul_ip': args.consul_ip,
		'consul_port': args.consul_port,
		'consul_service_name': args.consul_service_name,
		'consul_service_ip': args.consul_service_ip,
		'consul_service_port': args.consul_service_port,
	},
	'file': {
		'file_server_url': args.file_server_url,
	},
	'deploy': {
		'mode': args.deploy_mode,
	},
}
config = get_config()

# 更新配置（只覆盖提供的参数）
for section, values in config_updates.items():
	# 如果 section 不存在，先创建一个新的 section
	if section not in config:
		config[section] = {}

	for key, value in values.items():
		if value is not None and value != '':
			config[section][key] = str(value)

from app import create_app

app = create_app()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
