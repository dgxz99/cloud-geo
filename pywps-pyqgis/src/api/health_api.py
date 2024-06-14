import flask

# 创建flask蓝图
health_blue = flask.Blueprint('health', __name__)


@health_blue.route('/health')
def health_check():
	# 在这里执行健康检查逻辑，例如检查数据库连接、依赖服务等
	# 如果一切正常，返回HTTP 200状态码和一个表示健康的响应
	return flask.jsonify({"status": "healthy"}), 200
