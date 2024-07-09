import argparse
import atexit

import flask
from utils.consul_service import register_consul, deregister_consul
from api.pywps_api import pywps_blue, job_store_strategy
from api.health_api import health_blue
from api.file_api import file_blue
from api.provenance_api import provenance_blue
from context.config import get_config
from algorithm_init.init import init_database
from utils.job_task import start_cleanup_thread


def create_app():
	app = flask.Flask(__name__)

	# 注册蓝图
	app.register_blueprint(pywps_blue)
	app.register_blueprint(health_blue)
	app.register_blueprint(file_blue)
	app.register_blueprint(provenance_blue)

	return app


def main(config_parameters):
	# 读取配置
	deploy_mode = config_parameters.get('deploy_mode', None)  # 部署模式，默认为 None

	config = get_config()

	# 覆盖部署模式（如果命令行有提供）
	if deploy_mode:
		config['deploy']['mode'] = deploy_mode

	# 初始化算子库
	init_database()

	if config['deploy']['mode'] == 'distributed':
		# 获取consul相关配置
		service_name = config.get("consul", "service_name")
		service_ip = config.get("consul", "service_ip")
		service_port = config.getint("consul", "service_port")

		# 注册到consul
		register_consul(service_name, service_ip, service_port)
		atexit.register(deregister_consul, service_name, service_ip, service_port)

	# 创建 Flask 应用
	app = create_app()

	# 开启清理线程
	if config['deploy']['mode'] == 'single':
		start_cleanup_thread(job_store_strategy)

	# 运行 Flask 应用
	app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Run Flask app with specific configuration.')
	parser.add_argument('--deploy_mode', help='Deployment mode (e.g., single, distributed)')

	args = parser.parse_args()

	# 将命令行参数保存到字典中
	config_params = {
		'deploy_mode': args.deploy_mode,
	}
	main(config_params)
