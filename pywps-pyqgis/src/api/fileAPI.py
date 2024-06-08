import flask

file_blue = flask.Blueprint('file', __name__)


@file_blue.route('/outputs/' + '<path:filename>')
def outputfile(filename):
	target_file = os.path.join('outputs', filename)
	if os.path.isfile(target_file):
		file_ext = os.path.splitext(target_file)[1]
		if 'xml' in file_ext:
			mime_type = 'text/xml'
		else:
			mime_type = 'pywps_bluelication/octet-stream'
		# 设置响应头，告诉浏览器要下载文件，且适合下载大文件
		response = flask.send_file(target_file, mimetype=mime_type)
		response.headers["Content-Disposition"] = f"attachment; filename={filename}"
		print(f'\033[94m{filename}下载成功！\033[0m')
		return response
	else:
		flask.abort(404)


