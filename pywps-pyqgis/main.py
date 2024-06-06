import atexit
import configparser
import json
import os
import random

import flask
from flask import jsonify, request

from algorithm_init.mongo import MongoDB
from pywps import Service, configuration
from qgis.core import QgsApplication
from processes.QGISProFactory import QGISProcFactory

config_path = os.path.join(os.path.dirname(__file__), 'pywps.cfg')
config = configparser.ConfigParser()
config.read(config_path)

app = flask.Flask(__name__)
# 算子初始化
processes = QGISProcFactory().init_algorithms()

# For the process list on the home page
process_descriptor = {}
for process in processes:
	abstract = process.abstract
	process_descriptor[process.identifier] = abstract

# This is, how you start PyWPS instance
service = Service(processes, ['pywps.cfg'])


@app.route("/")
def hello():
	server_url = configuration.get_config_value("server", "url")
	request_url = flask.request.url
	return flask.render_template('home.html', request_url=request_url, server_url=server_url, process_descriptor=process_descriptor)


@app.route('/<base_url>', methods=['GET', 'POST'])
def wps_handle(base_url):
	return service


@app.route('/outputs/' + '<path:filename>')
def outputfile(filename):
	target_file = os.path.join('outputs', filename)
	if os.path.isfile(target_file):
		file_ext = os.path.splitext(target_file)[1]
		if 'xml' in file_ext:
			mime_type = 'text/xml'
		else:
			mime_type = 'application/octet-stream'
		# 设置响应头，告诉浏览器要下载文件，且适合下载大文件
		response = flask.send_file(target_file, mimetype=mime_type)
		response.headers["Content-Disposition"] = f"attachment; filename={filename}"
		print(f'\033[94m{filename}下载成功！\033[0m')
		return response
	else:
		flask.abort(404)


@app.route('/static/' + '<path:filename>')
def static_file(filename):
	target_file = os.path.join('static', filename)
	if os.path.isfile(target_file):
		with open(target_file, mode='rb') as f:
			file_bytes = f.read()
		mime_type = None
		return flask.Response(file_bytes, content_type=mime_type)
	else:
		flask.abort(404)


@app.route('/processes/<path:identifier>', methods=['GET'])
def describe_process(identifier):
	alg = MongoDB().find_one("algorithms", {"Identifier": identifier})
	if alg and '_id' in alg:
		alg['_id'] = str(alg['_id'])
	return jsonify(alg)


@app.route('/health')
def health_check():
	# 在这里执行健康检查逻辑，例如检查数据库连接、依赖服务等
	# 如果一切正常，返回HTTP 200状态码和一个表示健康的响应
	return jsonify({"status": "healthy"}), 200


@app.route('/list-algorithms', methods=['GET'])
def list_algorithms():
	algorithms = QgsApplication.processingRegistry().algorithms()

	algorithm_names = [algorithm.id() for algorithm in algorithms]
	return jsonify(algorithm_names)


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


@app.route('/publish-features', methods=['POST'])
def publish_features():
	"""
	接收POST请求，将vector_json_data保存到文件中
	Returns:
		None
	"""
	vector_json_data = json.loads(request.get_data())
	layer_name = generate_vector_name()
	with open(f"static/requests/temp_{layer_name}.json", "w") as file:
		json.dump(vector_json_data, file)
	return layer_name


from consul_service import register_consul, deregister_consul

service_name = config.get("consul", "service_name")
service_ip = config.get("consul", "service_ip")
service_port = config.getint("consul", "service_port")

register_consul(service_name, service_ip, service_port)
atexit.register(deregister_consul, service_name, service_ip, service_port)

if __name__ == "__main__":
	app.run()
