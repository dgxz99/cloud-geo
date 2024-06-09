import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import uuid

import flask
import requests

from dao.mongo import MongoDB
from pywps import Service, configuration
from qgis.core import QgsApplication
from processes.QGISProFactory import QGISProcFactory

# 算子初始化
processes = QGISProcFactory().init_algorithms()

# 在home页面查看process
process_descriptor = {}
for process in processes:
	abstract = process.abstract
	process_descriptor[process.identifier] = abstract

# PyWPS service实例
service = Service(processes, ['pywps.cfg'])

pywps_blue = flask.Blueprint('pywps', __name__)

# 创建线程池
executor = ThreadPoolExecutor(max_workers=4)


@pywps_blue.route("/")
def hello():
	server_url = configuration.get_config_value("server", "url")
	request_url = flask.request.url
	return flask.render_template('home.html', request_url=request_url, server_url=server_url, process_descriptor=process_descriptor)


# 存储任务状态和结果
job_status = {}
job_results = {}


def run_job(req, job_id):
	try:
		print(req)

		res = requests.post(req["req_base_url"], json=req["req_data"])
		job_status[job_id] = "Succeeded"
		job_results[job_id] = res
	except Exception as e:
		job_status[job_id] = f"Failed: {str(e)}"
		job_results[job_id] = None


@pywps_blue.route('/<base_url>', methods=['GET', 'POST'])
def wps_handle(base_url):
	flask_request = flask.request
	data = json.loads(flask_request.data)
	mode = data.get("mode", None)
	if mode:
		del data["mode"]
	job_id = str(uuid.uuid4())

	req = {
		"req_data": data,
		"req_method": flask_request.method,
		"req_base_url": "http://127.0.0.1:5000/jobs",
	}

	if mode == "async":
		job_status[job_id] = "Running"
		executor.submit(run_job, req, job_id)
		return flask.jsonify({'job-id': job_id})

	return service.call(flask_request)


@pywps_blue.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
	status = job_status.get(job_id, "Unknown job ID")
	return flask.jsonify({'job-id': job_id, 'status': status})


@pywps_blue.route('/processes/<path:identifier>', methods=['GET'])
def describe_process(identifier):
	alg = MongoDB().find_one("algorithms", {"Identifier": identifier})
	if alg and '_id' in alg:
		alg['_id'] = str(alg['_id'])
	return flask.jsonify(alg)


@pywps_blue.route('/health')
def health_check():
	# 在这里执行健康检查逻辑，例如检查数据库连接、依赖服务等
	# 如果一切正常，返回HTTP 200状态码和一个表示健康的响应
	return flask.jsonify({"status": "healthy"}), 200


@pywps_blue.route('/list-algorithms', methods=['GET'])
def list_algorithms():
	algorithms = QgsApplication.processingRegistry().algorithms()

	algorithm_names = [algorithm.id() for algorithm in algorithms]
	return flask.jsonify(algorithm_names)


def generate_vector_name():
	"""
	生成一个随机的矢量要素名称。
	Returns:
		vector_name (str): 随机生成的矢量名称。

	"""
	vector_name = ""
	for i in range(6):
		vector_name += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
	return vector_name


@pywps_blue.route('/publish-features', methods=['POST'])
def publish_features():
	"""
	接收POST请求，将vector_json_data保存到文件中
	Returns:
		None
	"""
	vector_json_data = json.loads(flask.request.get_data())
	layer_name = generate_vector_name()
	with open(f"static/requests/temp_{layer_name}.json", "w") as file:
		json.dump(vector_json_data, file)
	return layer_name
