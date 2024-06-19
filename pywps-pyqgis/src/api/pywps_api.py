import json
import os
import random
import time
import uuid
import flask

from concurrent.futures import ThreadPoolExecutor
from dao.mongo import MongoDB
from pywps import Service, configuration
from qgis.core import QgsApplication
from processes.QGISProFactory import QGISProcFactory
from strategy.job_store.JobStoreContext import JobStoreContext
from utils.job_task import run_job

# 配置上传目录
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../../inputs')

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)

# 算子初始化
processes = QGISProcFactory().init_algorithms()

# 准备所有文件夹
dir_list = ['logs', 'workdir', 'outputs']

for _dir in dir_list:
	if not os.path.exists(_dir):
		os.mkdir(_dir)
		print(f'{_dir} does not exist! Created it!')

# PyWPS service实例
service = Service(processes, ['pywps.cfg'])
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
		executor.submit(run_job, job_store_strategy, data, job_id)
		job_store_strategy.save_job(job_id, json.dumps(job_data))
		stored_job_data = json.loads(job_store_strategy.get_job(job_id))
		del stored_job_data['timestamp']
		if stored_job_data['result']:
			del stored_job_data['result']['jobId']
			del stored_job_data['result']['status']
		return json.dumps(stored_job_data)

	provenance = None
	wps_resp = service.call(flask_request).json
	try:
		for val in wps_resp['outputs']:
			if val.get('identifier') == 'provenance':
				provenance = json.loads(val.get('data').replace("'", "\""))
				break

		response = json.dumps({
			'jobId': job_id,
			'status': wps_resp['status']['status'],
			'completionTime': provenance['estimated_completion'],
			'expirationTime': provenance['estimated_completion'],
			'percentCompleted': wps_resp['status']['percent_done'],
			'message': wps_resp['status']['message'],
			'output': provenance['result']
		})
	except:
		response = json.dumps({
			'jobId': job_id,
			'status': wps_resp['status']['status'],
			'percentCompleted': wps_resp['status']['percent_done'],
			'message': wps_resp['status']['message'],
		})

	return response


@pywps_blue.route('/jobs/<job_id>', methods=['GET'])
def get_job_status(job_id):
	job_data = json.loads(job_store_strategy.get_job(job_id))
	if job_data:
		del job_data['timestamp']
		return flask.jsonify(job_data)
	else:
		return flask.jsonify({"error": "Job not found"}), 404


@pywps_blue.route('/processes', methods=['GET'])
def get_capabilities():
	flask_request = flask.request
	return service.call(flask_request)


@pywps_blue.route('/processes/<path:identifier>', methods=['GET'])
def describe_process(identifier):
	alg = MongoDB().find_one("algorithms", {"Identifier": identifier})
	if alg and '_id' in alg:
		alg['_id'] = str(alg['_id'])
	return flask.jsonify(alg)


@pywps_blue.route('/outputs/<path:filename>', methods=['GET'])
def outputfile(filename):
	if deploy_mode == 'single':
		output_dir = configuration.get_config_value("server", "outputpath")
		target_file = os.path.join(output_dir, filename)
		if os.path.isfile(target_file):
			file_ext = os.path.splitext(target_file)[1]
			if 'xml' in file_ext:
				mime_type = 'text/xml'
			else:
				mime_type = 'application/octet-stream'
			# 设置响应头，告诉浏览器要下载文件，且适合下载大文件
			response = flask.send_file(str(target_file), mimetype=mime_type)
			response.headers["Content-Disposition"] = f"attachment; filename={filename}"
			print(f'\033[94m{filename}下载成功！\033[0m')
			return response
	else:
		flask.abort(404)


# 上传文件接口
@pywps_blue.route('/upload', methods=['POST'])
def upload_file():
	if deploy_mode == 'single':
		if 'file' not in flask.request.files:
			return flask.jsonify({'error': 'No file part'}), 400
		file = flask.request.files['file']
		if file.filename == '':
			return flask.jsonify({'error': 'No selected file'}), 400
		if file:
			# 生成唯一的文件名
			filename = f"{uuid.uuid4().hex}_{file.filename}"
			file_path = os.path.join(UPLOAD_FOLDER, filename)
			file.save(file_path)
			return flask.jsonify({'message': 'File uploaded successfully', 'filename': filename}), 201
	else:
		flask.abort(404)


# 提供上传文件的访问URL
@pywps_blue.route('/inputs/<filename>')
def uploaded_file(filename):
	if deploy_mode == 'single':
		return flask.send_from_directory(UPLOAD_FOLDER, filename)
	else:
		flask.abort(404)


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
