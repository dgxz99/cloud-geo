from app.dao.mongo import MongoDB
from app.algorithm_init.process_alg_wps import get_algorithm_help, process_algorithm_info, convert_wps

from app.context.qgis import get_qgis


def init_database():
	# mongodb数据库连接
	mongo = MongoDB()
	# 每次初始化时删除已有的数据，重新初始化数据
	if len(mongo.find_all("algorithms")) != 0:
		print("删除算子数量为：", mongo.delete_all_documents("algorithms"), mongo.delete_all_documents("algorithms_qgs"))
	alg_list = get_qgis().processingRegistry().algorithms()
	for alg in alg_list:
		try:
			# 存储qgis算子原本描述信息
			alg_help = get_algorithm_help(alg)
			mongo.add_one("algorithms_qgs", {'identifier': alg.id(), 'description': alg_help})
			# 存储qgis算子wps2.0描述信息
			alg_wps = convert_wps(process_algorithm_info(alg_help))
			mongo.add_one("algorithms", alg_wps)
		except Exception as e:
			print(alg.id(), e)

	print(f"Database initialized! A total of algorithm {len(alg_list)}!")
