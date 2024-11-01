import io
import mimetypes
import re
import sys
import processing
from app.context.qgis import get_qgis
from app.algorithm_init.alg_wps2.algorithm import AlgorithmWPS, LiteralData, BoundingBoxData, ComplexData, Format


output_map = {
	"QgsProcessingOutputBoolean": {"wps_type": "LiteralOutput", "data_type": "boolean"},
	"QgsProcessingOutputNumber": {"wps_type": "LiteralOutput", "data_type": "float"},
	"QgsProcessingOutputFile": {"wps_type": "ComplexOutput", "data_type": "geographicData", "supported_formats": ["text/csv", "text/html"]},
	"QgsProcessingOutputFolder": {"wps_type": "LiteralOutput", "data_type": "string"},
	"QgsProcessingOutputHtml": {"wps_type": "ComplexOutput", "data_type": "geographicData", "supported_formats": ["text/html"]},
	"QgsProcessingOutputLayerDefinition": {},
	"QgsProcessingOutputMapLayer": {"wps_type": "ComplexOutput", "data_type": "geographicData", "supported_formats": ["image/tiff", "application/zip"]},
	"QgsProcessingOutputMultipleLayers": {"wps_type": "ComplexOutput", "data_type": "geographicData", "supported_formats": ["image/tiff", "application/zip"]},
	"QgsProcessingOutputPointCloudLayer": {},
	"QgsProcessingOutputRasterLayer": {"wps_type": "ComplexOutput", "data_type": "raster", "supported_formats": ["image/tiff"]},
	"QgsProcessingOutputString": {"wps_type": "LiteralOutput", "data_type": "string"},
	"QgsProcessingOutputVectorLayer": {"wps_type": "ComplexOutput", "data_type": "vector", "supported_formats": ["application/zip"]},
	"QgsProcessingOutputVectorTileLayer": {}
}

literal_type_map = {
	"maptheme": {"wps_type": "LiteralData", "data_type": "string"},
	"coordinateoperation": {"wps_type": "LiteralData", "data_type": "string"},
	"rasterDestination": {"wps_type": "LiteralData", "data_type": "string"},
	"number": {"wps_type": "LiteralData", "data_type": "float"},
	"raster_calc_expression": {"wps_type": "LiteralData", "data_type": "string"},
	"vectortilewriterlayers": {"wps_type": "LiteralData", "data_type": "string"},
	"aggregates": {"wps_type": "LiteralData", "data_type": "string"},
	"extent": {"wps_type": "LiteralData", "data_type": "string"},
	"enum": {"wps_type": "LiteralData", "data_type": "int"},
	"expression": {"wps_type": "LiteralData", "data_type": "string"},
	"crs": {"wps_type": "LiteralData", "data_type": "string"},
	"matrix": {"wps_type": "LiteralData", "data_type": "string"},
	"distance": {"wps_type": "LiteralData", "data_type": "float"},
	"databaseschema": {"wps_type": "LiteralData", "data_type": "string"},
	"boolean": {"wps_type": "LiteralData", "data_type": "boolean"},
	"meshdatasettime": {"wps_type": "LiteralData", "data_type": "string"},
	"idw_interpolation_data": {"wps_type": "LiteralData", "data_type": "string"},
	"databasetable": {"wps_type": "LiteralData", "data_type": "string"},
	"fields_mapping": {"wps_type": "LiteralData", "data_type": "string"},
	"OTBParameterChoice": {"wps_type": "LiteralData", "data_type": "string"},
	"meshdatasetgroups": {"wps_type": "LiteralData", "data_type": "string"},
	"range": {"wps_type": "LiteralData", "data_type": "string"},
	"providerconnection": {"wps_type": "LiteralData", "data_type": "string"},
	"multilayer": {"wps_type": "LiteralData", "data_type": "string"},
	"duration": {"wps_type": "LiteralData", "data_type": "string"},
	"layout": {"wps_type": "LiteralData", "data_type": "string"},
	"file": {"wps_type": "LiteralData", "data_type": "string"},
	"tininputlayers": {"wps_type": "LiteralData", "data_type": "string"},
	"dxflayers": {"wps_type": "LiteralData", "data_type": "string"},
	"scale": {"wps_type": "LiteralData", "data_type": "string"},
	"vectorDestination": {"wps_type": "LiteralData", "data_type": "string"},
	"folderDestination": {"wps_type": "LiteralData", "data_type": "string"},
	"string": {"wps_type": "LiteralData", "data_type": "string"},
	"fileDestination": {"wps_type": "LiteralData", "data_type": "string"},
	"field": {"wps_type": "LiteralData", "data_type": "string"},
	"layoutitem": {"wps_type": "LiteralData", "data_type": "string"},
	"band": {"wps_type": "LiteralData", "data_type": "int"},
	"relief_colors": {"wps_type": "LiteralData", "data_type": "string"},
	"execute_sql": {"wps_type": "LiteralData", "data_type": "string"},
	"color": {"wps_type": "LiteralData", "data_type": "string"},
	"point": {"wps_type": "LiteralData", "data_type": "string"}
}

complex_type_map = {
	"layer": {"wps_type": "ComplexData", "data_type": "geographicData"},
	"mesh": {"wps_type": "ComplexData", "data_type": "geographicData"},
	"rasterDestination": {"wps_type": "ComplexData", "data_type": "raster"},
	"source": {"wps_type": "ComplexData", "data_type": "vector"},
	"fileDestination": {"wps_type": "ComplexData", "data_type": "raster"},
	"multilayer": {"wps_type": "ComplexData", "data_type": "geographicData"},
	"sink": {"wps_type": "ComplexData", "data_type": "vector"},
	"file": {"wps_type": "ComplexData", "data_type": "geographicData"},
	"raster": {"wps_type": "ComplexData", "data_type": "raster"},
	"vector": {"wps_type": "ComplexData", "data_type": "vector"},
	"vectorDestination": {"wps_type": "ComplexData", "data_type": "vector"}
}


def get_algorithm_help(alg):
	"""
	从QGIS中获取算子帮助信息
	Args:
		alg: 算子对象
	Returns:
		算子的描述信息
	"""
	try:
		buffer = io.StringIO()
		sys.stdout = buffer
		processing.algorithmHelp(alg.id())
		alg_help = buffer.getvalue()
		return alg_help
	finally:
		sys.stdout = sys.__stdout__


def process_algorithm_info(alg_info):
	"""
	将算子描述信息转为json格式
	Args:
		alg_info: 算子的描述信息
	Returns:
		算子json格式的描述信息
	"""
	# 设置分隔符
	split_flag = "----------------\nInput parameters\n----------------"
	# 存储算子的字典
	alg_dict = {}

	# 将算子的描述信息分为两部分：[Title、Abstract、Identifier]
	alg_description_info = alg_info.split(split_flag)

	# 处理[Title、Abstract、Identifier]
	title_string = re.sub(r"\).*? \(", "*****", alg_description_info[0])
	title_list = title_string.split(")\n\n")
	alg_dict["Title"] = title_list[0].split("(")[0].strip()

	if "*****" in title_list[0]:
		identifier = title_list[0].split("*****")[1].strip()
	else:
		identifier = title_list[0].split("(")[1].strip()
	alg_dict["Abstract"] = alg_description_info[0].split(')\n\n', 1)[1].replace("\n", "")
	alg_dict["Identifier"] = identifier

	# 添加默认值信息和是否必要参数

	# 创建对应的算子对象
	alg = get_qgis().processingRegistry().createAlgorithmById(alg_dict.get("Identifier"))

	alg_dict["Inputs"] = []
	# 获取算子的输入参数
	input_parameters = alg.parameterDefinitions()
	# 添加输入参数信息并添加默认值和是否必要参数
	for param in input_parameters:
		input_param_dict = {
			"Title": param.name(),
			"Abstract": param.description(),
			"Identifier": param.name(),
			"Parameter type": type(param).__name__,
			"default_value": '' if param.defaultValue() is None else str(param.defaultValue()),
			"min_occurs": 0,
			"max_occurs": 1
		}

		if type(param).__name__ == "QgsProcessingParameterEnum":
			input_param_dict["Available values"] = [{str(index): value} for index, value in enumerate(param.options())]

		# 参数为空的情况下，判断是否为可选参数
		if not param.defaultValue() and param.defaultValue() != 0:
			flag = re.search(r'optional=(\w+)', param.asPythonString())
			if not flag:
				input_param_dict["min_occurs"] = 1  # 不是可选参数

		if param.type() == 'multilayer':
			input_param_dict["max_occurs"] = 10  # todo:考虑到内存原因，仅设置为10

		# OUTPUT参数不需要用户输入，系统指定，最后需要返回该URL
		if param in alg.destinationParameterDefinitions():
			input_param_dict["min_occurs"] = 0

		# 保存算子支持的文件格式
		try:
			file_type_str = param.createFileFilter()
			all_supported_files_match = re.search(r"All supported files(.*?);;", file_type_str)
			if all_supported_files_match:
				extensions = re.findall(r"\*(.\w+)", all_supported_files_match.group(0))
			else:
				extensions = re.findall(r"\*(.\w+)", file_type_str)

			unique_mime_types = set()  # 集合去重
			# 添加常见的GIS文件格式
			mimetypes.add_type("x-world/x-vrt", ".vrt")
			mimetypes.add_type('application/x-shapefile', '.shp')
			mimetypes.add_type('application/vnd.geo+json', '.geojson')
			mimetypes.add_type('application/vnd.google-earth.kml+xml', '.kml')
			mimetypes.add_type('application/vnd.google-earth.kmz', '.kmz')
			mimetypes.add_type('application/gpx+xml', '.gpx')
			mimetypes.add_type('image/tiff', '.tif')
			mimetypes.add_type('image/tiff', '.tiff')
			mimetypes.add_type('application/x-esri-grid', '.asc')
			mimetypes.add_type('application/x-hdf', '.hdf')
			mimetypes.add_type('application/x-netcdf', '.nc')
			mimetypes.add_type('application/x-erdas-imagine', '.img')
			mimetypes.add_type('application/x-grass-ascii-raster', '.asc')
			mimetypes.add_type('application/x-arcinfo-binary-coverage', '.adf')
			mimetypes.add_type('application/x-protobuf', '.mvt')
			mimetypes.add_type('application/x-shp-xml', '.shp.xml')
			mimetypes.add_type('application/x-sdat', '.sdat')
			for ext in extensions:
				mime_type, _ = mimetypes.guess_type(f'example{ext}')
				if mime_type:
					unique_mime_types.add(mime_type)
			if unique_mime_types:
				input_param_dict["wps_type"] = "ComplexInput"
				input_param_dict["data_type"] = complex_type_map[param.type()]["data_type"]
				input_param_dict["supported_formats"] = list(unique_mime_types)
			else:
				input_param_dict["wps_type"] = "LiteralInput"
				input_param_dict["data_type"] = literal_type_map[param.type()]["data_type"]
		except:
			input_param_dict["wps_type"] = "LiteralInput"
			input_param_dict["data_type"] = literal_type_map[param.type()]["data_type"]

		alg_dict["Inputs"].append(input_param_dict)

	# 获取算子的输出参数
	output_parameters = alg.outputDefinitions()
	alg_dict["Outputs"] = []

	for param in output_parameters:
		output_param_dict = {
			"Title": param.name(),
			"Abstract": param.description(),
			"Identifier": param.name(),
			"Parameter type": type(param).__name__,
			"wps_type": output_map.get(type(param).__name__).get("wps_type"),
		}
		if output_param_dict["wps_type"] == 'LiteralOutput':
			output_param_dict["data_type"] = output_map.get(type(param).__name__).get("data_type")
		elif output_param_dict["wps_type"] == 'ComplexOutput':
			output_param_dict["data_type"] = output_map.get(type(param).__name__).get("data_type")
			output_param_dict["supported_formats"] = output_map.get(type(param).__name__).get("supported_formats")
		alg_dict["Outputs"].append(output_param_dict)

	return alg_dict


def convert_wps(alg_dict):
	"""
	将算子转为符合WPS规范类型
	Args:
		alg_dict: 从文本信息中提取的算子字典
	Returns:
		符合WPS规范的算子描述信息
	"""
	title = alg_dict.get("Title")
	identifier = alg_dict.get("Identifier")
	abstract = alg_dict.get("Abstract")
	inputs = alg_dict.get("Inputs")
	outputs = alg_dict.get("Outputs")

	input_list = parameters_list(inputs)
	output_list = parameters_list(outputs)

	algorithm_wps = AlgorithmWPS(title=title, identifier=identifier, abstract=abstract, inputs=input_list, outputs=output_list)
	return algorithm_wps.to_dict()


def parameters_list(parameters):
	"""
	将参数根据映射规则从QGIS类型转换WPS类型
	Args:
		parameters: 参数列表：输入参数列表、输出参数列表
	Returns:
		符合WPS规范的参数列表
	"""
	parameter_list = []
	if len(parameters) != 0:
		for param in parameters:
			param_title = param.get("Title")
			param_abstract = param.get("Abstract")
			param_identifier = param.get("Identifier")
			available_values = param.get("Available values")
			default_value = param.get("default_value")
			min_occurs = param.get("min_occurs") if param.get("min_occurs") is not None else 1
			max_occurs = param.get("max_occurs") if param.get("max_occurs") is not None else 1
			wps_type = param.get("wps_type")
			data_type = param.get("data_type")
			supported_formats = param.get("supported_formats")

			param_data = None
			if wps_type in ["LiteralInput", "LiteralOutput"]:
				literal_data_domain = LiteralData.LiteralDataDomain(
					data_type=data_type, allowed_values=available_values, default_value=default_value, default=True
				)
				param_data = LiteralData(
					title=param_title, abstract=param_abstract, identifier=param_identifier,
					literal_data_domains=[literal_data_domain], min_occurs=min_occurs, max_occurs=max_occurs
				)
			elif wps_type in ["ComplexInput", "ComplexOutput"]:
				format_list = [Format(mime_type=item) for item in supported_formats]
				param_data = ComplexData(
					title=param_title, abstract=param_abstract, identifier=param_identifier,
					supported_format=format_list, min_occurs=min_occurs, max_occurs=max_occurs
				)
			elif wps_type in ["BoundingBoxInput", "BoundingBoxOutput"]:  # todo: supported_crs这个是不能为空的，但目前并未遇到有这种参数类型
				param_data = BoundingBoxData(
					title=param_title, abstract=param_abstract, identifier=param_identifier, supported_crs=[], min_occurs=min_occurs, max_occurs=max_occurs
				)
			parameter_list.append(param_data)
	return parameter_list

# if __name__ == '__main__':
# 	# 初始化QGIS算子，保证能够正常调用
# 	QgsApplication.setPrefixPath(r"D:\GIS\QGIS", True)
# 	qgs = QgsApplication([], False)
# 	qgs.initQgis()
# 	Processing().initialize()
#
# 	# 获取算子对象
# 	algorithm = qgs.processingRegistry().createAlgorithmById("gdal:gdal2tiles")
# 	algorithm_help = get_algorithm_help(algorithm)
# 	info = process_algorithm_info(algorithm_help)
# 	print(info)
# 	print(convert_wps(info))
