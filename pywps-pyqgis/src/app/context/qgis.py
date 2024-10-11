# Windows下导入QGIS环境
# def import_qgis_plugin():
# 	import sys
# 	import platform
# 	if platform.system() == 'Windows':
# 		sys.path.append('C:/Program Files/QGIS 3.28.15/apps/qgis-ltr/python/plugins')
# 	else:
# 		sys.path.append('/usr/share/qgis/python/plugins')
#
#
# import_qgis_plugin()
import processing
from qgis.core import *
from processing.core.ProcessingConfig import ProcessingConfig, Setting

import platform
if platform.system() == 'Windows':
	OTB_PATH = r'D:\Widgets\OTB'
	OTB_APP_PATH = r'D:\Widgets\OTB\lib\otb\applications'
else:
	OTB_PATH = r'/opt/otb'
	OTB_APP_PATH = r'/opt/otb/lib/otb/applications'


# 获取QGIS全局对象
def get_qgis():
	if not hasattr(get_qgis, 'qgs'):
		# 初始化QGIS算子，保证能够正常调用
		get_qgis.qgs = QgsApplication([], False)
		get_qgis.qgs.initQgis()

		# 创建otb配置对象
		otb_setting = Setting(ProcessingConfig.tr('General'), 'OTB_FOLDER', ProcessingConfig.tr('OTB installation folder'), True)
		# 指定otb的所在目录
		otb_setting.value = OTB_PATH

		# 创建otb应用程序配置对象
		otb_app_setting = Setting(ProcessingConfig.tr('General'), 'OTB_APP_FOLDER', ProcessingConfig.tr('OTB application folder'), True)
		# 指定otb应用目录
		otb_app_setting.value = OTB_APP_PATH

		# 加载otb配置到QGIS Processing
		ProcessingConfig().addSetting(otb_setting)
		ProcessingConfig().addSetting(otb_app_setting)

		# 初始化Processing
		processing.Processing().initialize()
		print("Algorithm initialized!")
	return get_qgis.qgs
