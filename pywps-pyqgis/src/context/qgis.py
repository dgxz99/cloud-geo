# Windows下导入QGIS环境
# def import_qgis_plugin():
# 	import sys
# 	sys.path.append('C:/Program Files/QGIS 3.28.15/apps/qgis-ltr/python/plugins')
#
# import_qgis_plugin()
import processing
from qgis.core import *

qgs = None


# 获取QGIS全局对象
def get_qgis():
	global qgs
	if not qgs:
		# 初始化QGIS算子，保证能够正常调用
		qgs = QgsApplication([], False)
		qgs.initQgis()
		processing.Processing().initialize()
		print("algorithm initialized")

	return qgs