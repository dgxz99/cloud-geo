import json
import os.path

from .process_alg_wps import get_algorithm_help, convert_wps, process_algorithm_info
from ..context.qgis import get_qgis


def save_json():
	for alg in get_qgis().processingRegistry().algorithms():
		alg_help = get_algorithm_help(alg)
		alg_wps = convert_wps(process_algorithm_info(alg_help))
		if not os.path.exists('app/algorithm_init/json_datas'):
			os.mkdir('app/algorithm_init/json_datas')

		# 保存数据到文件
		with open("app/algorithm_init/json_datas/{}.json".format(alg_wps.get("Identifier").replace(":", "_")), "w", encoding="utf-8") as file:
			try:
				json.dump(alg_wps, file)
			except Exception:
				print(alg_wps.get("Identifier"))
				print(alg_wps)


if __name__ == '__main__':
	save_json()
