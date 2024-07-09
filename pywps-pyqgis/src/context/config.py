import configparser
import os


def get_config_file_path():
	"""
	获取配置文件绝对路径
	Returns:
		配置文件绝对路径
	"""
	return os.path.abspath(os.path.join(os.getcwd(), 'pywps.cfg'))


def get_config():
	"""
	获取配置文件对象
	Returns:
		配置文件对象
	"""
	if not hasattr(get_config, "config"):
		config_path = get_config_file_path()
		config = configparser.ConfigParser()
		config.read(config_path)
		get_config.config = config
		print("Config initialized!")
	return get_config.config
