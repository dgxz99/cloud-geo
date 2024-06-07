import os

from processes.strategy.OutputHandlerParams import OutputHandlerParams
from processes.strategy.TextOutputHandlerStrategy import TextOutputHandlerStrategy
from processes.strategy.FileOutputHandlerStrategy import FileOutputHandlerStrategy
from processes.strategy.DirectoryOutputHandlerStrategy import DirectoryOutputHandlerStrategy


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
            strategy.handle(params)
        else:
            raise ValueError(f"No strategy found for output type: {output_type}")

    def _determine_output_type(self, params: OutputHandlerParams):
        if isinstance(params.output_data, str):
            if os.path.isdir(params.output_data):
                return "directory"
            elif os.path.isfile(params.output_data):
                return "file"
            else:
                return "str"
        else:
            raise ValueError("Unsupported output type")
