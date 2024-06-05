import os
from qgis.core import QgsVectorFileWriter, QgsProject
from processes.strategy.OutputHandlerParams import OutputHandlerParams
from processes.strategy.OutputHandlerStrategy import OutputHandlerStrategy


class VectorMemoryOutputHandlerStrategy(OutputHandlerStrategy):
	def handle(self, params: OutputHandlerParams):
		vector_layer = params.result[params.output_name]
		save_path = os.path.join(params.output_dir, f"{params.output_file_name}.gpkg")

		save_options = QgsVectorFileWriter.SaveVectorOptions()
		save_options.driverName = 'GPKG'  # 指定驱动程序名称为 GPKG
		save_options.fileEncoding = 'UTF-8'

		# 使用 writeAsVectorFormatV3 保存矢量图层到 GeoPackage
		QgsVectorFileWriter.writeAsVectorFormatV3(
			vector_layer, save_path, QgsProject.instance().transformContext(), save_options
		)
		params.response.outputs[params.output_name].data = params.output_url + f"{params.output_file_name}.gpkg"
