#!/bin/bash

# 版本号
qgis_version=3.28.15
qgis_full_version=1:${qgis_version}+36jammy
# 安装的软件列表
qgis_app_list=(qgis python3-qgis python3-qgis-common libqgis-customwidgets qgis-providers qgis-providers-common qgis-common qgis-plugin-grass qgis-plugin-grass-common qgis-provider-grass)
qgis_lib_list=(libqgis-3d libqgis-core libqgis-analysis libqgis-app libqgis-gui libqgis-native libqgis-server libqgispython libqgisgrass7-)

# 修改依赖库包名
for i in $(seq 0 $(expr ${#qgis_lib_list[*]} - 1)); do
	qgis_lib_list[i]=${qgis_lib_list[i]}${qgis_version}
done

# 限定安装的软件包版本
qgis_app_install_list=()
for i in $(seq 0 $(expr ${#qgis_app_list[*]} - 1)); do
	qgis_app_install_list[i]=${qgis_app_list[i]}=${qgis_full_version}
done

# 执行安装并锁定版本
apt install -y ${qgis_app_install_list[*]} ${qgis_lib_list[*]}
apt-mark hold ${qgis_app_list[*]} ${qgis_lib_list[*]}
