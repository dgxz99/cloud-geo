import json
import os
import random
import uuid

import flask
from qgis.core import QgsApplication
from config import get_config

# 配置上传目录
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'inputs')

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
	os.makedirs(UPLOAD_FOLDER)
	print('inputs does not exist! Created it!')

# 读取部署模式
config = get_config()
deploy_mode = config.get('deploy', 'mode')

# 创建flask蓝图
file_blue = flask.Blueprint('file', __name__)


@file_blue.route('/outputs/<path:filename>', methods=['GET'])
def outputfile(filename):
	if deploy_mode == 'single':
		output_dir = config.get("server", "outputpath")
		target_file = os.path.join(os.getcwd(), output_dir, filename)
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
			# 文件不存在，返回404错误
			print(f'\033[91m{filename}不存在！\033[0m')
			return flask.jsonify({"error": f"{filename} does not exist."}), 404
	else:
		return flask.jsonify({'error': 'Resource not found.'}), 404


# 上传文件接口
@file_blue.route('/upload', methods=['POST'])
def upload_file():
	if deploy_mode == 'single':
		if 'file' not in flask.request.files:
			return flask.jsonify({'error': 'No file part'}), 400
		# 获取所有上传的文件
		files = flask.request.files.getlist('file')
		if len(files) == 0:
			return flask.jsonify({'error': 'No selected file'}), 400

		saved_files = []
		for file in files:
			if file.filename == '':
				return flask.jsonify({'error': 'One or more files without a name were uploaded'}), 400
			if file:
				# 生成唯一的文件名
				filename = f"{uuid.uuid4().hex}_{file.filename}"
				file_path = os.path.join(UPLOAD_FOLDER, filename)
				file.save(file_path)
				saved_files.append(filename)
		return flask.jsonify({'message': 'Files uploaded successfully', 'filenames': saved_files}), 201
	else:
		return flask.jsonify({'error': 'Resource not found.'}), 404


# 提供上传文件的访问URL
@file_blue.route('/inputs/<filename>')
def uploaded_file(filename):
	if deploy_mode == 'single':
		return flask.send_from_directory(UPLOAD_FOLDER, filename)
	else:
		return flask.jsonify({'error': 'Resource not found.'}), 404


@file_blue.route('/list-algorithms', methods=['GET'])
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


@file_blue.route('/publish-features', methods=['POST'])
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
