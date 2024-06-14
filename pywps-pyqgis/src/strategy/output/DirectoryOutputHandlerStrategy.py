import os

from strategy.output.OutputHandlerParams import OutputHandlerParams
from strategy.output.OutputHandlerStrategy import OutputHandlerStrategy


class DirectoryOutputHandlerStrategy(OutputHandlerStrategy):

	def handle(self, params: OutputHandlerParams):
		filename = f"{os.path.basename(params.output_data)}.zip"
		zip_path = os.path.join(params.output_dir, filename)
		self.zip_folder(params.output_data, zip_path)

		if params.deploy_mode == 'distributed':
			output_file = self.upload_file(params.output_url, zip_path)
			return f'{params.output_url}/retrieve/{output_file}'
		else:
			return params.output_url + filename

