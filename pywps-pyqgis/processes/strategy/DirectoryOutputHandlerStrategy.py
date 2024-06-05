import os

from processes.strategy.OutputHandlerParams import OutputHandlerParams
from processes.strategy.OutputHandlerStrategy import OutputHandlerStrategy


class DirectoryOutputHandlerStrategy(OutputHandlerStrategy):

	def handle(self, params: OutputHandlerParams):
		self.zip_folder(params.output_data, os.path.join(params.output_dir, f"{os.path.basename(params.output_data)}.zip"))
		params.response.outputs[params.output_name].data = params.output_url + f'{params.output_file_name}.zip'
