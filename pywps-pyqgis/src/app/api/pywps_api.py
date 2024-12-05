import json
import os
import time
import uuid
import flask

from config import get_config, get_config_file_path
from concurrent.futures import ThreadPoolExecutor
from app.dao.mongo import MongoDB
from pywps import Service
from pywps.exceptions import NoApplicableCode

from app.processes.QGISProFactory import QGISProcFactory
from app.strategy.job_store.JobStoreContext import JobStoreContext
from app.utils.job_task import run_job
from app.utils.json_response import JsonResponse

# 算子初始化
processes = QGISProcFactory().init_algorithms()

# 准备所有文件夹
dir_list = ['logs', 'workdir', 'outputs']

for _dir in dir_list:
	if not os.path.exists(_dir):
		os.mkdir(_dir)
		print(f'{_dir} does not exist! Created it!')

# PyWPS service实例
service = Service(processes, [get_config_file_path()])
# 读取部署模式
config = get_config()
deploy_mode = config.get('deploy', 'mode')
job_store_strategy = JobStoreContext(deploy_mode).job_store_strategy()
# 创建线程池
executor = ThreadPoolExecutor()

# 创建flask蓝图
pywps_blue = flask.Blueprint('pywps', __name__)


@pywps_blue.route('/jobs', methods=['POST'])
def execute():
	flask_request = flask.request
	data = json.loads(flask_request.data)  # 请求体
	mode = data.get("mode", None)
	job_id = data.get("job_id", None)
	if job_id is None:
		job_id = uuid.uuid4().hex
	if mode == "async":
		del data["mode"]  # 删除异步表示，防止递归请求
		job_data = {
			"jobId": job_id,
			"status": "Running",
			"result": None,
			"timestamp": time.time()
		}
		# 异步执行算子
		executor.submit(run_job, job_store_strategy, data, job_id)
		job_store_strategy.save_job(job_id, json.dumps(job_data))
		stored_job_data = json.loads(job_store_strategy.get_job(job_id))
		del stored_job_data['timestamp']
		return JsonResponse.success(data=stored_job_data)

	try:
		wps_response = service.call(flask_request)
		if isinstance(wps_response, NoApplicableCode):
			raise wps_response
		wps_resp = wps_response.json

		provenance = {}
		for val in wps_resp['outputs']:
			if val.get('identifier') == 'provenance':
				provenance = json.loads(val.get('data').replace("'", "\""))
				break

		# 存储 provenance
		provenance["_id"] = job_id
		mongo = MongoDB()
		w3c_prov = to_w3c_prov(provenance)
		mongo.add_one('provenance', w3c_prov)
		mongo.close()

		response = {
			'jobId': job_id,
			'status': wps_resp['status']['status'],
			'completionTime': provenance['estimated_completion'],
			'expirationTime': provenance['expiration_time'],
			'percentCompleted': wps_resp['status']['percent_done'],
			'message': wps_resp['status']['message'],
			'output': provenance['result']
		}
	except Exception as e:
		response = {
			'jobId': job_id,
			'status': "failed",
			'message': "Failed to execute process",
			"result": str(e),
		}

	return JsonResponse.success(data=response)


def to_w3c_prov(prov):
	return {
		"_id": prov['_id'],
		"executor": {"identifier": prov['name'], "type": "Executor"},
		"entities": [
			{
				"type": "Params",
				"value": prov['params']
			},
			{
				"type": "Results",
				"value": prov['result']
			}
		],
		"activities": [
			{
				"type": "Execute",
				"attributes": {
					"startTime": prov['start_time'],
					"estimatedCompletion": prov['estimated_completion'],
					"expirationTime": prov['expiration_time'],
					"runTime": prov["run_time"],
					"status": prov['status']
				}
			}
		],
		"relationships": [
			{"type": "generated", "source": "Execute", "target": "Result"},
			{"type": "used", "source": "Execute", "target": "Params"},
			{"type": "responsibleFor", "source": "Executor", "target": "Execute"}
		],
		"context": {
			"project": "CloudGeoPy",
			"process": f"{prov['name']} Operation",
			"environment": "PyWPS with PyQGIS backend",
			"version": "1.0.0"
		}
	}


@pywps_blue.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
	job_json = job_store_strategy.get_job(job_id)
	if job_json:
		job_data = json.loads(job_json)
		if 'timestamp' in job_data:
			del job_data['timestamp']
			if job_data['status'] != 'Running':
				del job_data['result']['jobId']
				del job_data['result']['status']
		return JsonResponse.success(job_data)
	else:
		return JsonResponse.error(data={"message": "Job not found"})


@pywps_blue.route('/results/<job_id>', methods=['GET'])
def get_job_results(job_id):
	job_json = job_store_strategy.get_job(job_id)
	if job_json:
		ret = json.loads(job_json)
		if ret['result'] is None and ret['status'] == 'Running':
			return JsonResponse.success(data={"message": "Job is still running"})
		return JsonResponse.success(data=ret['result'])
	else:
		return JsonResponse.error(data={"message": "Job not found"})


@pywps_blue.route('/processes', methods=['GET'])
def get_capabilities():
	flask_request = flask.request
	pywps_resp = service.call(flask_request).json

	response = {
		"service": "CloudGeoPy",
		"version": "1.0.0",
		"title": pywps_resp["title"],
		"abstract": pywps_resp["abstract"],
		"keywords": pywps_resp["keywords"],
		"keywords_type": pywps_resp["keywords_type"],
		# "provider": pywps_resp["provider"],
		"contents": [{"Title": p["title"], "Abstract": p["abstract"], "Identifier": p["identifier"]} for p in pywps_resp["processes"]]
	}
	return JsonResponse.success(data=response)


@pywps_blue.route('/processes/<path:identifier>', methods=['GET'])
def describe_process(identifier):
	mongo = MongoDB()
	alg = mongo.get_one("algorithms", {"Identifier": identifier})
	if alg and '_id' in alg:
		alg['_id'] = str(alg['_id'])
	mongo.close()
	return JsonResponse.success(data=alg)
