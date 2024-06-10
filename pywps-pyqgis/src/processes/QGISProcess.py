# from context.qgis import import_qgis_plugin
# import_qgis_plugin()
import logging
import time
import uuid
import zipfile
import os
import mimetypes
import re
import pywps.configuration
from processes.strategy.OutputHandlerContext import OutputHandlerContext
from processes.strategy.OutputHandlerParams import OutputHandlerParams
from pywps import Process, LiteralInput, ComplexInput
from processing.core.Processing import processing
from qgis.core import *
from pywps.app.exceptions import ProcessError

# QgsApplication.setPrefixPath(r"D:\GIS\QGIS", True)
# qgs = QgsApplication([], False)
# qgs.initQgis()
# print('qgs initialized')
# Processing().initialize()
# print('algorithm initialized')

LOGGER = logging.getLogger("PYWPS")


class QGISProcess(Process):
	def __init__(self, identifier, title, abstract, inputs, outputs):
		super(QGISProcess, self).__init__(
			handler=self._handler,
			identifier=str(identifier),
			title=str(title),
			abstract=str(abstract),
			version='1.3.3.7',
			inputs=inputs,
			outputs=outputs,
			store_supported=True,
			status_supported=True
		)

	def _handler(self, request, response):
		# 显式地调用ogr.UseExceptions()来设置异常处理的方式，防止终端输出FutureWarning
		from osgeo import ogr
		ogr.UseExceptions()

		temp_dir = self.workdir
		output_dir = pywps.configuration.get_config_value("server", "outputpath")
		output_url = pywps.configuration.get_config_value("file", "file_server_url")
		output_file_name = None

		try:
			# 构建算法参数
			algorithm_params = {}
			alg = QgsApplication.processingRegistry().createAlgorithmById(self.identifier)

			for param in self.inputs:
				if 'OUTPUT' in param.identifier:
					parameter = next(filter(lambda para: para.name() == param.identifier, alg.parameterDefinitions()), None)
					output_file_name = f"{self.identifier.replace(':', '-')}-{param.identifier.lower()}-{uuid.uuid4()}"
					if isinstance(param, ComplexInput):
						# 正则表达式匹配文件扩展名，使用 findall 方法查找所有匹配的扩展名
						extensions = re.findall(r"\*\.(\w+)", parameter.createFileFilter())
						# 矢量文件以shp文件保存并打包
						if extensions[0].lower() == 'gpkg':
							os.mkdir(os.path.join(temp_dir, output_file_name))
							ret_data = os.path.join(temp_dir, output_file_name, f"{output_file_name}.shp")
						else:
							ret_data = os.path.join(output_dir, f'{output_file_name}.{extensions[0]}')
						algorithm_params[param.identifier] = ret_data

					# 针对于算子输出参数为目录的情况
					elif isinstance(parameter, QgsProcessingParameterFolderDestination):
						algorithm_params[param.identifier] = os.path.join(temp_dir, output_file_name)

				# 若该参数未传值
				input_data = request.inputs.get(param.identifier)
				if input_data is None:
					continue

				if isinstance(param, ComplexInput):
					self._handle_complex_input(algorithm_params, param, input_data, temp_dir)
				elif isinstance(param, LiteralInput):
					self._handle_literal_input(algorithm_params, param, input_data)

			# 打印参数信息
			print("algorithm_params:", algorithm_params)
			LOGGER.info(f"algorithm_name: {self.identifier}")
			start_time = time.time()
			LOGGER.info(f"算子启动于: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time))}")
			LOGGER.info(f"algorithm_params: {algorithm_params}")

			# 调用 QGIS 算法执行逻辑，使用 algorithm_identifier 执行算法
			ret = processing.run(self.identifier, algorithm_params)

			LOGGER.info(f"算子运行时长: {time.time() - start_time}")

			# 初始化输出文件上下文管理器
			output_handler_context = OutputHandlerContext()
			# 处理输出文件
			for param_name, ret_data in ret.items():
				if ret_data:
					output_params = OutputHandlerParams(
						self.identifier, algorithm_params, param_name, ret_data,
						response, output_dir, output_url, output_file_name
					)
					output_handler_context.handle_output(output_params)

			print(f'\033[94m{self.identifier} run success!\033[0m')  # 终端蓝色打印，成功执行算子
			LOGGER.info(f"{self.identifier}运行成功!")
			LOGGER.info(f"Result: {ret}")

		except Exception as e:
			# 处理异常
			print(f'\033[93m{self.identifier} run error!\033[0m')  # 终端黄色打印，算子执行失败
			LOGGER.error(f"{self.identifier}运行发生错误!")
			raise ProcessError(f"算子运行时发生错误: {str(e)}")

		return response

	def _handle_literal_input(self, algorithm_params, param, input_data):
		"""
		处理LiteralInput参数
		Args:
			algorithm_params: 算子参数字典
			param: 算子中的参数对象
			input_data: 参数的输入数据
		"""
		algorithm_params[param.identifier] = input_data[0].data

	def _handle_complex_input(self, algorithm_params, param, input_data, temp_dir):
		"""
		处理ComplexInput参数
		Args:
			algorithm_params: 算子参数字典
			param: 算子中的参数对象
			input_data: 参数的输入数据
			temp_dir: 临时文件夹
		"""
		# mime_type
		mime_types = [fmt.mime_type for fmt in param.supported_formats]
		param_files = [item.file for item in input_data]
		# 校验文件格式是否输入正确
		for param_file in param_files:
			file_mimetype, _ = mimetypes.guess_type(param_file)
			if file_mimetype not in mime_types:
				raise ProcessError(f"传入文件格式有误，{param.identifier}只能传入{mime_types}类型数据！")

		# 根据输入参数的最大出现次数不同实现相应的处理
		if param.max_occurs == 1:
			if param_files[0].endswith(".zip"):
				result_files = self.find_shp_files(param_files[0], temp_dir)
				algorithm_params[param.identifier] = result_files[0]
			else:
				algorithm_params[param.identifier] = param_files[0]
		else:
			algorithm_params[param.identifier] = []
			for param_file in param_files:
				if param_file.endswith(".zip"):
					result_files = self.find_shp_files(param_file, temp_dir)
					algorithm_params[param.identifier].extend(result_files)
				else:
					algorithm_params[param.identifier].append(param_file)

	@staticmethod
	def find_shp_files(zip_file, directory):
		"""
		获取压缩包中'.shp' 扩展名的文件路径
		Args:
			zip_file: 压缩包文件路径
			directory: 解压目录
		Returns:
			.shp扩展名的文件路径列表
		"""
		with zipfile.ZipFile(zip_file, 'r') as zip_ref:
			zip_ref.extractall(directory)
		shp_files = []
		for root, dirs, files in os.walk(directory):
			for file in files:
				if file.endswith('.shp'):
					shp_files.append(os.path.join(root, file))
		return shp_files