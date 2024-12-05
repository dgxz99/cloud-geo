import json


class JsonResponse:
	"""
	统一的json返回格式
	"""

	def __init__(self, data, success, msg):
		self.data = data
		self.success = success
		self.msg = msg

	@classmethod
	def success(cls, data=None, success=True, msg='success'):
		return json.dumps(cls(data, success, msg).to_dict())

	@classmethod
	def error(cls, data=None, success=False, msg='error'):
		return json.dumps(cls(data, success, msg).to_dict())

	def to_dict(self):
		return {
			"success": self.success,
			"msg": self.msg,
			"data": self.data
		}
