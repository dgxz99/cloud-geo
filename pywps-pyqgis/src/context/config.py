import configparser
import os


def get_config():
	"""
	获取配置文件对象
	Returns:
		配置文件对象
	"""
	if not hasattr(get_config, "config"):
		config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'pywps.cfg')
		config = configparser.ConfigParser()
		config.read(config_path)
		get_config.config = config
		print("Config initialized!")
	return get_config.config
