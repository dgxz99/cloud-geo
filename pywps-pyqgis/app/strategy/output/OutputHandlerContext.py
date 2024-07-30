import os

from app.strategy.output.OutputHandlerParams import OutputHandlerParams
from app.strategy.output.TextOutputHandlerStrategy import TextOutputHandlerStrategy
from app.strategy.output.FileOutputHandlerStrategy import FileOutputHandlerStrategy
from app.strategy.output.DirectoryOutputHandlerStrategy import DirectoryOutputHandlerStrategy


class OutputHandlerContext:
    def __init__(self):
        self._strategies = {
            "directory": DirectoryOutputHandlerStrategy(),
            "str": TextOutputHandlerStrategy(),
            "file": FileOutputHandlerStrategy()
        }

    def handle_output(self, params: OutputHandlerParams):
        output_type = self._determine_output_type(params)
        strategy = self._strategies.get(output_type)
        if strategy:
            return strategy.handle(params)
        else:
            raise ValueError(f"No strategy found for output type: {output_type}")

    @staticmethod
    def _determine_output_type(params: OutputHandlerParams):
        if isinstance(params.output_data, str):
            if os.path.isdir(params.output_data):
                return "directory"
            elif os.path.isfile(params.output_data):
                return "file"
            else:
                return "str"
        else:
            raise ValueError("Unsupported output type")
