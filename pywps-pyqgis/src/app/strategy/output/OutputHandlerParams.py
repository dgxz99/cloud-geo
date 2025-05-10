class OutputHandlerParams:
    def __init__(self, identifier, algorithm_params, output_name, output_data, response, output_dir, output_url, output_file_names, deploy_mode=None):
        """
        Args:
            identifier: 算子的唯一标识符
            algorithm_params: 算子的输入参数（字典）
            output_name: 输出参数名称
            output_data: 输出参数数据
            response: PyWPS返回的响应
            output_dir: 结果文件保存的路径（文件夹）
            output_url: 结果文件的URL
            output_file_names: 输出文件的名称的字典
        """
        self.identifier = identifier
        self.algorithm_params = algorithm_params
        self.output_name = output_name
        self.output_data = output_data
        self.response = response
        self.output_dir = output_dir
        self.output_url = output_url
        self.output_file_names = output_file_names
        self.deploy_mode = deploy_mode
