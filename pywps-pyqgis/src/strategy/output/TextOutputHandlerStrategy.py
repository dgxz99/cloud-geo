from strategy.output.OutputHandlerParams import OutputHandlerParams
from strategy.output.OutputHandlerStrategy import OutputHandlerStrategy


class TextOutputHandlerStrategy(OutputHandlerStrategy):
	def handle(self, params: OutputHandlerParams):
		return params.output_data
