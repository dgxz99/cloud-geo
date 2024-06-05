import json
import processing
from qgis.core import *
from mongo import MongoDB
from process_alg_wps import get_algorithm_help, process_algorithm_info, convert_wps

if __name__ == '__main__':
	# 初始化QGIS算子，保证能够正常调用
	QgsApplication.setPrefixPath(r"D:\GIS\QGIS", True)
	qgs = QgsApplication([], False)
	qgs.initQgis()
	processing.Processing().initialize()
	print("algorithm initialized")

	# mongodb数据库连接
	mongo = MongoDB()
	# 每次初始化时删除已有的数据，重新初始化数据
	if len(mongo.find_all("algorithms")) != 0:
		print(mongo.delete_all_documents("algorithms"))

	for alg in qgs.processingRegistry().algorithms():
		alg_help = get_algorithm_help(alg)
		try:
			alg_wps = convert_wps(process_algorithm_info(alg_help))
		except:
			print(alg.id())
			print(alg_help)
			break

		# 保存数据到文件
		with open("./datas/{}.json".format(alg_wps.get("Identifier").replace(":", "_")), "w", encoding="utf-8") as file:
			try:
				json.dump(alg_wps, file)
			except Exception:
				print(alg_wps.get("Identifier"))
				print(alg_wps)

		# 存储数据到数据库
		mongo.add_one("algorithms", alg_wps)

	# 关闭数据库连接
	mongo.close()
