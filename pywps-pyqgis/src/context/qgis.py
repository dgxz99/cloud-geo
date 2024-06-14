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


# 获取QGIS全局对象
def get_qgis():
	if not hasattr(get_qgis, 'qgs'):
		# 初始化QGIS算子，保证能够正常调用
		get_qgis.qgs = QgsApplication([], False)
		get_qgis.qgs.initQgis()
		processing.Processing().initialize()
		print("Algorithm initialized!")
	return get_qgis.qgs
