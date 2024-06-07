import configparser
import os

config = None


def get_config():
	global config
	if config == None:
		config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'pywps.cfg')
		config = configparser.ConfigParser()
		config.read(config_path)
		print("config init!")
	return config
