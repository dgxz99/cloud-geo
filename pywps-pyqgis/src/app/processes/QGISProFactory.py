from app.processes.QGISProcess import QGISProcess
from pywps.validator.mode import MODE
from app.dao.mongo import MongoDB
from pywps import LiteralInput, LiteralOutput, ComplexInput, ComplexOutput, Format, BoundingBoxOutput, BoundingBoxInput


class QGISProcFactory:
	mongo = MongoDB()
	algorithms = mongo.find_all("algorithms")
	mongo.close()

	@classmethod
	def init_algorithms(cls):
		process_list = []
		for alg in cls.algorithms:
			try:
				input_list = cls.create_parameters(alg["Input"], is_input=True)
				output_list = cls.create_parameters(alg["Output"], is_input=False)
				process_list.append(
					QGISProcess(identifier=alg.get("Identifier"), title=alg.get("Title"), abstract=alg.get("Abstract"), inputs=input_list, outputs=output_list)
				)
			except Exception as e:
				print(e)
				print(alg.get("Identifier"))
		return process_list

	@staticmethod
	def create_parameters(params, is_input=True):
		parameter_list = []
		for param in params:
			data_type = param["DataType"]
			param_info = {
				"title": param.get("Title"),
				"abstract": param.get("Abstract"),
				"identifier": param.get("Identifier"),
				"keywords": param.get("keywords"),
				"metadata": param.get("Metadata"),
				"mode": MODE.NONE
			}

			if data_type == "ComplexData":
				format_list = param["ComplexData"]["Format"]
				param_info["supported_formats"] = [Format(item["mimeType"]) for item in format_list]
				if is_input:
					param_info["min_occurs"] = param.get("minOccurs")
					param_info["max_occurs"] = param.get("maxOccurs")
					parameter_list.append(ComplexInput(**param_info))
				else:
					parameter_list.append(ComplexOutput(**param_info))

			elif data_type == "LiteralData":
				literal_data_domain_list = param.get("LiteralData").get("LiteralDataDomain")
				literal_data_domain = None
				if len(literal_data_domain_list) == 1:
					literal_data_domain = literal_data_domain_list[0]
				else:
					for item in literal_data_domain_list:
						if str(item.get("default")) == "True":
							literal_data_domain = item

				param_info["data_type"] = "string"
				param_info["uoms"] = literal_data_domain.get("UOM")

				if is_input:
					param_info["min_occurs"] = param.get("minOccurs")
					param_info["max_occurs"] = param.get("maxOccurs")
					# param_info["default"] = literal_data_domain.get("DefaultValue")
					param_info["allowed_values"] = literal_data_domain.get("AllowedValues")
					parameter_list.append(LiteralInput(**param_info))
				else:
					parameter_list.append(LiteralOutput(**param_info))

			elif data_type == "BoundingBoxData":
				param_info["crss"] = param["BoundingBoxData"].get("SupportedCRS")
				if is_input:
					param_info["min_occurs"] = param.get("minOccurs")
					param_info["max_occurs"] = param.get("maxOccurs")
					parameter_list.append(BoundingBoxInput(**param_info))
				else:
					parameter_list.append(BoundingBoxOutput(**param_info))

		return parameter_list


if __name__ == '__main__':
	cls = QGISProcFactory()
	print(len(cls.init_algorithms()))
