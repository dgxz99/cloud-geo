import os
import zipfile
from abc import ABC, abstractmethod

import requests

from processes.strategy.OutputHandlerParams import OutputHandlerParams


class OutputHandlerStrategy(ABC):
	@abstractmethod
	def handle(self, params: OutputHandlerParams):
		pass

	@staticmethod
	def zip_folder(folder_path, zip_path):
		"""
		压缩文件夹至指定路径
		Args:
			folder_path: 被压缩的文件夹
			zip_path: 压缩文件保存的路径
		"""
		# 创建一个 ZIP 压缩文件对象
		with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
			# 遍历文件夹中的所有文件和子文件夹
			for root, dirs, files in os.walk(folder_path):
				for file in files:
					# 构建文件的绝对路径
					file_path = os.path.join(root, file)
					# 构建文件在压缩文件中的相对路径
					rel_path = os.path.relpath(str(file_path), folder_path)
					# 将文件添加到压缩文件中
					zipf.write(str(file_path), rel_path)

	@staticmethod
	def upload_file(url, file_path):
		upload_url = url + '/upload'
		with open(file_path, 'rb') as f:
			response = requests.put(upload_url, files={'file': f})
		response.raise_for_status()
		data = response.json()["data"]
		output_file_name = data["name"]
		output_file_ext = data["format"]
		return output_file_name + '.' + output_file_ext
