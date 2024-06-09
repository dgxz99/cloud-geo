import os
import shutil
import uuid

from processes.strategy.OutputHandlerParams import OutputHandlerParams
from processes.strategy.OutputHandlerStrategy import OutputHandlerStrategy


class FileOutputHandlerStrategy(OutputHandlerStrategy):
	def handle(self, params: OutputHandlerParams):
		ext = os.path.splitext(params.output_data)[1][1:]  # 获取文件扩展名
		if ext in ['shp', 'gpkg']:  # 矢量文件格式
			filename = f"{params.output_file_name}.zip"
			file_path = os.path.join(params.output_dir, filename)
			self.zip_folder(os.path.dirname(params.output_data), file_path)
		else:
			# 默认文件输出（没有输入输出文件的位置）
			if params.output_name not in [param for param in params.algorithm_params] or params.output_data != params.algorithm_params[params.output_name]:
				filename = f"{params.identifier.replace(':', '-')}-{params.output_name.lower().replace('_', '-')}-{uuid.uuid4()}.{ext}"
				file_path = os.path.join(params.output_dir, filename)
				shutil.move(params.output_data, file_path)
			else:
				# 输出栅格等单一文件
				filename = os.path.basename(params.output_data)
				file_path = os.path.join(params.output_dir, filename)
		output_file = self.upload_file(params.output_url, filename, file_path)
		params.response.outputs[params.output_name].data = f'{params.output_url}/retrieve/{output_file}'
		os.remove(file_path)  # 删除本地文件
