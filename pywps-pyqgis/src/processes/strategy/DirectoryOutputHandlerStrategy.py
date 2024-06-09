import os

from processes.strategy.OutputHandlerParams import OutputHandlerParams
from processes.strategy.OutputHandlerStrategy import OutputHandlerStrategy


class DirectoryOutputHandlerStrategy(OutputHandlerStrategy):

	def handle(self, params: OutputHandlerParams):
		filename = f"{os.path.basename(params.output_data)}.zip"
		zip_path = os.path.join(params.output_dir, filename)
		self.zip_folder(params.output_data, zip_path)
		output_file = self.upload_file(params.output_url, filename, zip_path)
		params.response.outputs[params.output_name].data = f'{params.output_url}/retrieve/{output_file}'
		os.remove(zip_path)
