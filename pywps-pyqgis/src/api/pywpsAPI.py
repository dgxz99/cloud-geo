import json
import random
import flask

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


@pywps_blue.route("/")
def hello():
	server_url = configuration.get_config_value("server", "url")
	request_url = flask.request.url
	return flask.render_template('home.html', request_url=request_url, server_url=server_url, process_descriptor=process_descriptor)


@pywps_blue.route('/<base_url>', methods=['GET', 'POST'])
def wps_handle(base_url):
	return service


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
