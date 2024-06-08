import os
import shutil
import uuid

from processes.strategy.OutputHandlerParams import OutputHandlerParams
from processes.strategy.OutputHandlerStrategy import OutputHandlerStrategy


class FileOutputHandlerStrategy(OutputHandlerStrategy):
	def handle(self, params: OutputHandlerParams):
		ext = os.path.splitext(params.output_data)[1][1:]  # 获取文件扩展名
		if ext in ['shp', 'gpkg']:  # 矢量文件格式
			file_path = os.path.join(params.output_dir, f"{params.output_file_name}.zip")
			self.zip_folder(os.path.dirname(params.output_data), file_path)
		else:
			# 默认文件输出（没有输入输出文件的位置）
			if params.output_name not in [param for param in params.algorithm_params] or params.output_data != params.algorithm_params[params.output_name]:
				file_name = f"{params.identifier.replace(':', '-')}-{params.output_name.lower().replace('_', '-')}-{uuid.uuid4()}.{ext}"
				file_path = os.path.join(params.output_dir, file_name)
				shutil.move(params.output_data, file_path)
			else:
				# 输出栅格等单一文件
				file_path = os.path.join(params.output_dir, os.path.basename(params.output_data))
		output_file = self.upload_file(params.output_url, file_path)
		params.response.outputs[params.output_name].data = f'{params.output_url}/retrieve/{output_file}'
		os.remove(file_path)  # 删除本地文件
