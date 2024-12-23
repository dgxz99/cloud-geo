import atexit
import flask
from config import get_config
from .algorithm_init.init import init_database
from .utils.job_task import start_cleanup_thread
from .utils.consul_service import register_consul, deregister_consul


def create_app():
	app = flask.Flask(__name__)

	# 初始化算子库
	init_database()

	# 局部导入，防止还未完成数据的初始化
	from .api import config_blueprint
	from .api.pywps_api import job_store_strategy

	# 注册blueprint
	config_blueprint(app)

	# 获取配置
	config = get_config()

	# 开启清理线程
	if config['deploy']['mode'] == 'single':
		start_cleanup_thread(job_store_strategy)

	if config['deploy']['mode'] == 'distributed':
		# 获取consul相关配置
		service_name = config.get("consul", "consul_service_name")
		service_ip = config.get("consul", "consul_service_ip")
		service_port = config.getint("consul", "consul_service_port")

		# 注册到consul
		register_consul(service_name, service_ip, service_port)

		# 退出时注销服务
		atexit.register(deregister_consul, service_name, service_ip, service_port)

	# 运行 Flask 应用
	return app
