# Open source GIS operator environment

An open source GIS operator environment, based on Ubuntu 22.04 (jammy) version of the production, which contains the following open source environment and operators:

- QGIS 3.28.15 (including GRASS and GDAL operators)
- Orfeo Toolbox 9.0.0
- Saga 7.3.0

The `tag` format of the image is: `QGIS version - OTB version - Saga version`.

## Usage

You can build a mirror of the open source operator service based on this mirror, or you can call the corresponding operator directly in it via the PyQGIS API.

When using PyQGIS, all the operators have been automatically loaded into the QGIS provider except for the OTB's operators, for the OTB's operators need to be loaded manually in the Python script, here is an example:

```python
/bin/python3 /bin/python3
from qgis.core import QgsApplication
import processing
from processing.core.ProcessingConfig import ProcessingConfig, Setting

# Instantiate the QGIS application object
qgs = QgsApplication([], False)

# Create otb configuration object
otb_setting = Setting(ProcessingConfig.tr('General'), 'OTB_FOLDER', ProcessingConfig.tr('OTB installation folder'), True)
# Specify the directory where otb is located, inside the container it is located in /opt/otb.
otb_setting.value = '/opt/otb'

# Create the otb application configuration object
otb_app_setting = Setting(ProcessingConfig.tr('General'), 'OTB_APP_FOLDER', ProcessingConfig.tr('OTB application folder'), True)
# Specify the otb application folder, located in /opt/otb/lib/otb/applications in the container.
otb_app_setting.value = '/opt/otb/lib/otb/applications'

# Load otb configuration into QGIS Processing
ProcessingConfig().addSetting(otb_setting)
ProcessingConfig().addSetting(otb_app_setting)

# Initialize Processing
processing.Processing().initialize()

# Iterate through and print all providers
for provider in qgs.processingRegistry().providers():
	print(provider.name(), 'provides', len(provider.algorithms()), 'algorithms')

# Print the full number of operators
print(len(qgs.processingRegistry().algorithms()))
``
```