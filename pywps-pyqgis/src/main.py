import atexit
import os.path

# 准备所有文件夹
dir_list = ['logs', 'workdir', 'outputs']
for dir in dir_list:
	if not os.path.exists(dir):
		os.mkdir(dir)
		print(f'{dir} is not exists! Created it!')

import flask
from utils.consul_service import register_consul, deregister_consul
from api.pywpsAPI import pywps_blue
from context.config import get_config
from algorithm_init.init import init_database

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

# 注册pywps_blue
app.register_blueprint(pywps_blue, url_prefix='')

if __name__ == "__main__":
	app.run()