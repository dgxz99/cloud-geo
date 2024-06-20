# 开源GIS算子环境

一个开源的GIS算子环境，基于Ubuntu 22.04 (jammy)版本制作，其中包含以下开源的环境和算子：

- QGIS 3.28.15（包含GRASS和GDAL算子）
- Orfeo Toolbox 9.0.0
- Saga 7.3.0

镜像的`tag`格式为：`QGIS版本-OTB版本-Saga版本`

## 使用方法

可以基于该镜像构建开源算子服务的镜像，也可以直接在其中通过PyQGIS API调用对应的算子。

在使用PyQGIS时，除了OTB的算子之外，其余算子均已自动加载到QGIS提供者中，对于OTB的算子需要在Python脚本中手动加载，下面是一个示例：

```python
#!/bin/python3
from qgis.core import QgsApplication
import processing
from processing.core.ProcessingConfig import ProcessingConfig, Setting

# 实例化QGIS应用对象
qgs = QgsApplication([], False)
# 创建otb配置对象
otb_setting = Setting(
ProcessingConfig.tr('General'), 'OTB_FOLDER', ProcessingConfig.tr('OTB installation folder'), True)
# 指定otb的所在目录，容器内位于/opt/otb
otb_setting.value = "/opt/otb"
# 加载otb配置到QGIS Processing
ProcessingConfig().addSetting(otb_setting)
# 初始化Processing
processing.Processing().initialize()

# 遍历打印所有提供者
for provider in qgs.processingRegistry().providers():
	print(provider.name(), 'provides', len(provider.algorithms()), 'algorithms')

# 打印全部算子数量
print(len(qgs.processingRegistry().algorithms()))
```