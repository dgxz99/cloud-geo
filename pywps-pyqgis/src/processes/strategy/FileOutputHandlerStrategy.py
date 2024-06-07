import os
import shutil
import uuid

from processes.strategy.OutputHandlerParams import OutputHandlerParams
from processes.strategy.OutputHandlerStrategy import OutputHandlerStrategy


class FileOutputHandlerStrategy(OutputHandlerStrategy):
	def handle(self, params: OutputHandlerParams):
		ext = os.path.splitext(params.output_data)[1][1:]  # 获取文件扩展名
		if ext in ['shp', 'gpkg']:  # 矢量文件格式
			zip_path = os.path.join(params.output_dir, f"{params.output_file_name}.zip")
			self.zip_folder(os.path.dirname(params.output_data), zip_path)
			params.response.outputs[params.output_name].data = params.output_url + f'{params.output_file_name}.zip'
		else:
			if params.output_name not in [param for param in params.algorithm_params] or params.output_data == params.algorithm_params[params.output_name]:
				dst_file_name = f"{params.identifier.replace(':', '-')}-{params.output_name.lower()}-{uuid.uuid4()}.{ext}"
				shutil.move(params.output_data, os.path.join(params.output_dir, dst_file_name))
				params.response.outputs[params.output_name].data = params.output_url + dst_file_name
			else:
				params.response.outputs[params.output_name].data = params.output_url + os.path.basename(params.output_data)
