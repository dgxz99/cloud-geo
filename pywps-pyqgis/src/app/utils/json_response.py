import json


class JsonResponse:
	"""
	统一的json返回格式
	"""

	def __init__(self, data, code, msg):
		self.data = data
		self.code = code
		self.msg = msg

	@classmethod
	def success(cls, data=None, code=1, msg='success'):
		return json.dumps(cls(data, code, msg).to_dict())

	@classmethod
	def error(cls, data=None, code=-1, msg='error'):
		return json.dumps(cls(data, code, msg).to_dict())

	def to_dict(self):
		return {
			"code": self.code,
			"msg": self.msg,
			"data": self.data
		}
