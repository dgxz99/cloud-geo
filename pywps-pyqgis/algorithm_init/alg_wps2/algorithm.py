from abc import ABC, abstractmethod


class Format:
	def __init__(self, mime_type, encoding='UTF-8', schema='', max_megabytes=None, default=False):
		"""
		Args:
			mime_type: 数据类型
			encoding: 编码方式
			schema: 数据结构
			max_megabytes: 数据最大大小
			default: 是否为默认数据类型
		"""

		self.mime_type = mime_type
		self.encoding = encoding
		self.schema = schema
		self.max_megabytes = max_megabytes
		self.default = default

	def to_dict(self):
		return {
			"mimeType": self.mime_type,
			"encoding": self.encoding,
			"schema": self.schema,
			"maximumMegabytes": self.max_megabytes,
			"default": self.default
		}


class Parameter(ABC):
	def __init__(self, title, abstract, identifier, keywords=None, metadata=None, min_occurs=1, max_occurs=1):
		self.title = title
		self.identifier = identifier
		self.abstract = abstract
		self.keywords = keywords if keywords is not None else []
		self.metadata = metadata if metadata is not None else []
		self.min_occurs = min_occurs
		self.max_occurs = max_occurs

	@abstractmethod
	def to_dict(self):
		pass

	def common_to_dict(self):
		return {
			"Title": self.title,
			"Abstract": self.abstract,
			"Identifier": self.identifier,
			"Keywords": self.keywords,
			"Metadata": self.metadata,
			"minOccurs": self.min_occurs,
			"maxOccurs": self.max_occurs,
		}

	@staticmethod
	def enforce_default_parameter(param_list):
		if param_list:
			default_count = sum(1 for param in param_list if param.default)
			if default_count == 0:
				param_list[0].default = True
			elif default_count > 1:
				raise ValueError("参数的默认数据格式只能有一个！")


class ComplexData(Parameter):
	def __init__(self, title, identifier, supported_format, abstract='', keywords=None, metadata=None, min_occurs=1, max_occurs=1):
		"""
		Args:
			title: 标题  -> str
			abstract: 简短描述  -> str
			identifier: 唯一标识符 -> str
			keywords:  描述参数的关键字 -> list
			metadata: 其他描述信息 -> list
			min_occurs: 最小出现次数，默认为1 -> int
			max_occurs: 最大出现次数，默认为1 -> int
			supported_format: 支持的数据格式 -> list
		"""
		super().__init__(title, abstract, identifier, keywords, metadata, min_occurs, max_occurs)
		self.enforce_default_parameter(supported_format)
		self.format_info = supported_format

	def to_dict(self):
		data_dict = self.common_to_dict()
		format_dicts = [format_info.to_dict() for format_info in self.format_info]
		data_dict.update({
			"DataType": "ComplexData",
			"ComplexData": {
				"Format": format_dicts
			}
		})
		return data_dict


class LiteralData(Parameter):
	class LiteralDataDomain:
		def __init__(self, data_type, allowed_values=None, uom=None, default_value=None, default=False):
			"""
			Args:
				data_type: 数据类型
				allowed_values: 允许的数据值
				uom: 数据单位
				default_value: 数据默认值
				default: 是否为默认文本数据域
			"""
			self.allowed_values = allowed_values if allowed_values is not None else []
			self.data_type = data_type
			self.uom = uom
			self.default_value = default_value
			self.default = default

		def to_dict(self):
			domain_dict = {
				"AllowedValues": self.allowed_values,
				"DataType": {
					"reference": f"http://www.w3.org/2001/XMLSchema#{self.data_type}",
					"content": self.data_type
				},
				"UOM": self.uom,
				"DefaultValue": self.default_value,
				"default": self.default
			}
			return domain_dict

	def __init__(self, title, identifier, literal_data_domains, abstract='', keywords=None, metadata=None, supported_format=None, min_occurs=1, max_occurs=1):
		"""
		Args:
			title: 标题 -> str
			abstract: 简短描述 -> str
			identifier: 唯一标识符 -> str
			keywords:  描述参数的关键字 -> list
			metadata: 其他描述信息 -> list
			min_occurs : 最小出现次数，默认为1-> int
			max_occurs: 最大出现次数，默认为1 -> int
			supported_format: 支持的数据格式  -> list
			literal_data_domains: 支持的文本域格式  -> list
		"""
		super().__init__(title, abstract, identifier, keywords, metadata, min_occurs, max_occurs)
		# self.enforce_default_parameter(supported_format)
		self.format_info = supported_format if supported_format is not None else []
		self.enforce_default_parameter(literal_data_domains)
		self.literal_data_domains = literal_data_domains

	def to_dict(self):
		data_dict = self.common_to_dict()
		format_dicts = [format_info.to_dict() for format_info in self.format_info]
		literal_data_domain_dicts = [domain.to_dict() for domain in self.literal_data_domains]
		data_dict.update({
			"DataType": "LiteralData",
			"LiteralData": {
				"Format": format_dicts,
				"LiteralDataDomain": literal_data_domain_dicts
			}
		})
		return data_dict


class BoundingBoxData(Parameter):
	class SupportedCRS:
		def __init__(self, crs, default=False):
			"""
			Args:
				crs: 坐标系 -> str
				default: 是否为默认坐标系，默认值为False -> boolean
			"""
			self.crs = crs
			self.default = default

		def to_dict(self):
			crs_dict = {
				"CRS": self.crs,
				"default": self.default
			}
			return crs_dict

	def __init__(self, title, identifier, supported_crs, abstract='', keywords=None, metadata=None, supported_format=None, min_occurs=1, max_occurs=1):
		"""
		Args:
			title: 标题 -> str
			abstract: 简短描述 -> str
			identifier: 唯一标识符 -> str
			keywords:  描述参数的关键字 -> list
			metadata: 其他描述信息 -> list
			min_occurs: 最小出现次数，默认为1 -> int
			max_occurs: 最大出现次数，默认为1 -> int
			supported_format: 支持的数据格式 -> list
			supported_crs:支持的坐标系格式 -> list
		"""
		super().__init__(title, abstract, identifier, keywords, metadata, min_occurs, max_occurs)
		# self.enforce_default_parameter(supported_format)
		self.format_info = supported_format if supported_format is not None else []
		self.enforce_default_parameter(supported_crs)
		self.supported_crs_list = supported_crs

	def to_dict(self):
		data_dict = self.common_to_dict()
		format_dicts = [format_info.to_dict() for format_info in self.format_info]
		crs_dicts = [crs.to_dict() for crs in self.supported_crs_list]
		data_dict.update({
			"DataType": "BoundingBoxData",
			"BoundingBoxData": {
				"Format": format_dicts,
				"SupportedCRS": crs_dicts
			}
		})
		return data_dict


class AlgorithmWPS:
	def __init__(self, identifier, title, abstract='', keywords=None, metadata=None, inputs=None, outputs=None):
		"""
		Args:
			title: 算子标题 -> str
			abstract: 算子功能简短描述 -> str
			identifier: 算子唯一标识符 -> str
			keywords:  描述算子的关键字 -> list
			metadata: 其他描述信息，一般以简单链接的方式存储；如：{"title": "","href": "","role": "","type": ""} -> list
			inputs: 算子的输入参数 -> list
			outputs: 算子的输出参数 -> list
		"""
		self.identifier = identifier
		self.title = title
		self.abstract = abstract
		self.keywords = keywords if keywords is not None else []
		self.metadata = metadata if metadata is not None else []
		self.inputs = inputs if inputs is not None else []
		self.outputs = outputs if outputs is not None else []

	def to_dict(self):
		input_dicts = [input_param.to_dict() for input_param in self.inputs]
		output_dicts = [output_param.to_dict() for output_param in self.outputs]
		return {
			"Title": self.title,
			"Abstract": self.abstract,
			"Identifier": self.identifier,
			"Keywords": self.keywords,
			"Metadata": self.metadata,
			"Input": input_dicts,
			"Output": output_dicts
		}


if __name__ == '__main__':
	pass
