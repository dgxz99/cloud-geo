import json
import os
import time
import uuid
import flask

from concurrent.futures import ThreadPoolExecutor
from dao.mongo import MongoDB
from pywps import Service, configuration
from context.config import get_config_file_path

from processes.QGISProFactory import QGISProcFactory
from strategy.job_store.JobStoreContext import JobStoreContext
from utils.job_task import run_job

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
deploy_mode = configuration.get_config_value('deploy', 'mode')
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
		future = executor.submit(run_job, job_store_strategy, data, job_id)
		job_store_strategy.save_job(job_id, json.dumps(job_data))
		stored_job_data = json.loads(job_store_strategy.get_job(job_id))
		ret = future.result()
		job_store_strategy.del_job(ret['jobId'])
		del stored_job_data['timestamp']
		return json.dumps(stored_job_data)

	provenance = None
	wps_resp = service.call(flask_request).json
	try:
		for val in wps_resp['outputs']:
			if val.get('identifier') == 'provenance':
				provenance = json.loads(val.get('data').replace("'", "\""))
				break

		response = {
			'jobId': job_id,
			'status': wps_resp['status']['status'],
			'completionTime': provenance['estimated_completion'],
			'expirationTime': provenance['expiration_time'],
			'percentCompleted': wps_resp['status']['percent_done'],
			'message': wps_resp['status']['message'],
			'output': provenance['result']
		}
	except:
		response = {
			'jobId': job_id,
			'status': wps_resp['status']['status'],
			'percentCompleted': wps_resp['status']['percent_done'],
			'message': wps_resp['status']['message'],
		}

	job_store_strategy.save_job(job_id, json.dumps({'result': response}))
	provenance["_id"] = job_id
	MongoDB().add_one('provenance', provenance)
	return json.dumps(response)


@pywps_blue.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
	job_json = job_store_strategy.get_job(job_id)
	if job_json:
		job_data = json.loads(job_json)
		if 'timestamp' in job_data:
			del job_data['timestamp']
			del job_data['result']['jobId']
			del job_data['result']['status']
		return json.dumps(job_data)
	else:
		return flask.jsonify({"error": "Job not found"}), 404


@pywps_blue.route('/results/<job_id>', methods=['GET'])
def get_job_results(job_id):
	job_json = job_store_strategy.get_job(job_id)
	if job_json:
		ret = json.loads(job_json)
		if ret['result']:
			return json.dumps(ret['result'])
	else:
		return flask.jsonify({"error": "Job not found"}), 404


@pywps_blue.route('/processes', methods=['GET'])
def get_capabilities():
	flask_request = flask.request
	pywps_resp = service.call(flask_request).json

	response = json.dumps({
		"service": "WPS",
		"version": "2.0",
		"title": pywps_resp["title"],
		"abstract": pywps_resp["abstract"],
		"keywords": pywps_resp["keywords"],
		"keywords_type": pywps_resp["keywords_type"],
		"provider": pywps_resp["provider"],
		"contents": [{"Title": p["title"], "Abstract": p["abstract"], "Identifier": p["identifier"]} for p in pywps_resp["processes"]]
	})
	return response


@pywps_blue.route('/processes/<path:identifier>', methods=['GET'])
def describe_process(identifier):
	alg = MongoDB().find_one("algorithms", {"Identifier": identifier})
	if alg and '_id' in alg:
		alg['_id'] = str(alg['_id'])
	return json.dumps(alg)
