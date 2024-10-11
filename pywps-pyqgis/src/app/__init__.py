import atexit

import flask
from .utils.consul_service import register_consul, deregister_consul
from .api.pywps_api import job_store_strategy
from .context.config import get_config
from .algorithm_init.init import init_database
from .utils.job_task import start_cleanup_thread
from .api import config_blueprint


def create_app(config_parameters=None):
    app = flask.Flask(__name__)
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

    # 注册blueprint
    config_blueprint(app)

    # 开启清理线程
    if config['deploy']['mode'] == 'single':
        start_cleanup_thread(job_store_strategy)

    # 运行 Flask 应用
    return app
