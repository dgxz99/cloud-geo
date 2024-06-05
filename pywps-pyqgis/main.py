import json
import os
import random

import flask
from flask import jsonify, request

from algorithm_init.mongo import MongoDB
from pywps import Service, configuration
from qgis.core import QgsApplication
from processes.QGISProFactory import QGISProcFactory

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
	"""
		This function parses the request URL and extracts the following:
			default operation, process identifier, output_ids, default mimetype
			info that cannot be terminated from the URL will be None (default)

			The url is expected to be in the following format, all the levels are optional.
			[base_url]/[identifier]/[output_ids]

		:return: dict with the extracted info listed:
			base_url - [wps|processes|jobs|api/api_level]
			default_mimetype - determinate by the base_url part:
				XML - if the base url == 'wps',
				JSON - if the base URL in ['api'|'jobs'|'processes']
			operation - also determinate by the base_url part:
				['api'|'jobs'] -> 'execute'
				processes -> 'describeProcess' or 'getCapabilities'
					'describeProcess' if identifier is present as the next item, 'getCapabilities' otherwise
			api - api level, only expected if base_url=='api'
			identifier - the process identifier
			output_ids - if exist then it selects raw output with the name output_ids
	"""
	return service


# @app.route('/api/alg', methods=['POST'])
# def test_pyqgs_alg():
# 	# 获取请求中的JSON数据
# 	# data = request.get_json()
# 	inp = [r"C:\Users\admin\Desktop\PyWPS\算子实验数据\gdal_merge\INPUT\srtm_58_05.tif", r"C:\Users\admin\Desktop\PyWPS\算子实验数据\gdal_merge\INPUT\srtm_59_05.tif"]
# 	outp = rf'C:\Users\admin\Desktop\PyWPS\data\temp\{uuid.uuid4()}.tif'
# 	try:
# 		processing.run("gdal:merge", {'INPUT': inp, 'OUTPUT': outp})
# 		return jsonify({"success": "run success!"}), 200
# 	except:
# 		return jsonify({"error": "run error!"}), 400


@app.route('/outputs/' + '<path:filename>')
def outputfile(filename):
	target_file = os.path.join('outputs', filename)
	if os.path.isfile(target_file):
		file_ext = os.path.splitext(target_file)[1]
		if 'xml' in file_ext:
			mime_type = 'text/xml'
		else:
			mime_type = 'application/octet-stream'
		# return flask.Response(file_bytes, content_type=mime_type)
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


@app.route('/description/<path:identifier>', methods=['GET'])
def describe_process(identifier):
	alg = MongoDB().find_one("algorithms", {"Identifier": identifier})
	if alg and '_id' in alg:
		alg['_id'] = str(alg['_id'])
	return jsonify(alg)


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


if __name__ == "__main__":
	app.run()
# import argparse
#
# parser = argparse.ArgumentParser(
# 	description="""Script for starting an example PyWPS instance with sample processes""",
# 	epilog="""Do not use this service in a production environment.
# 	It's intended to be running in test environment only!
# 	For more documentation, visit http://pywps.org/doc
# 	"""
# )
# parser.add_argument('-d', '--daemon', action='store_true', help="run in daemon mode")
# parser.add_argument(
# 	'-a',
# 	'--all-addresses',
# 	action='store_true',
# 	help="run flask using IPv4 0.0.0.0 (all network interfaces), otherwise bind to 127.0.0.1 (localhost). This maybe necessary in systems that only run Flask")
# args = parser.parse_args()
#
# if args.all_addresses:
# 	bind_host = '0.0.0.0'
# else:
# 	bind_host = '127.0.0.1'
#
# if args.daemon:
# 	pid = None
# 	try:
# 		pid = os.fork()
# 	except OSError as e:
# 		raise Exception("%s [%d]" % (e.strerror, e.errno))
#
# 	if pid == 0:
# 		os.setsid()
# 		app.run(threaded=True, host=bind_host)
# 	else:
# 		os._exit(0)
# else:
# 	app.run(threaded=True, host=bind_host)
