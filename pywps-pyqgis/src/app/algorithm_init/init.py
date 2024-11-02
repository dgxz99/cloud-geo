import time

from app.dao.mongo import MongoDB
from app.algorithm_init.process_alg_wps import get_algorithm_help, process_algorithm_info, convert_wps

from app.context.qgis import get_qgis


def init_database():
	algorithms_qgs = []  # QGIS原始算子描述信息
	algorithms = []  # WPS2.0算子描述信息

	# 获取所有算子
	alg_list = get_qgis().processingRegistry().algorithms()
	for alg in alg_list:
		try:
			alg_help = get_algorithm_help(alg)
			algorithms_qgs.append({'Identifier': alg.id(), 'description': alg_help})
			# 转为WPS2.0格式
			alg_wps = convert_wps(process_algorithm_info(alg_help))
			algorithms.append(alg_wps)
		except Exception as e:
			print(alg.id(), e)

	# mongodb数据库连接
	mongo = MongoDB()
	lock_name = 'database_init_lock'

	while True:
		lock = mongo.acquire_lock(lock_name)
		if lock:
			try:
				mongo.add_many("algorithms", algorithms)
				mongo.add_many("algorithms_qgs", algorithms_qgs)
				print(f"Database initialized! A total of algorithm {len(mongo.find_all('algorithms'))}!")
				break
			finally:
				mongo.release_lock(lock_name)
		else:
			print("Another process is initializing the database. Waiting...")
			time.sleep(3)

	mongo.close()
