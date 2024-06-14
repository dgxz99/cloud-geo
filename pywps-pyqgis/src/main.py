import atexit
import os.path

import flask
from utils.consul_service import register_consul, deregister_consul
from api.pywps_api import pywps_blue, job_store_strategy, deploy_mode
from api.health_api import health_blue
from context.config import get_config
from algorithm_init.init import init_database
from utils.job_task import start_cleanup_thread

# 准备所有文件夹
dir_list = ['logs', 'workdir', 'outputs']
for _dir in dir_list:
	if not os.path.exists(_dir):
		os.mkdir(_dir)
		print(f'{_dir} is not exists! Created it!')

# 读取配置
config = get_config()

# 初始化算子库
init_database()

# 获取consul相关配置
service_name = config.get("consul", "service_name")
service_ip = config.get("consul", "service_ip")
service_port = config.getint("consul", "service_port")

# 注册到consul
register_consul(service_name, service_ip, service_port)
atexit.register(deregister_consul, service_name, service_ip, service_port)

app = flask.Flask(__name__)

# 注册蓝图
app.register_blueprint(pywps_blue)
app.register_blueprint(health_blue)

if __name__ == "__main__":
	# 开启清理线程
	if deploy_mode == 'single':
		start_cleanup_thread(job_store_strategy)
	app.run()
