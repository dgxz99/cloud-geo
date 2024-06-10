#!/bin/bash
version=1:3.28.15+17bookworm
version_simple=3.28.15

apt install -y qgis=${version} qgis-plugin-grass=${version} qgis-plugin-grass-common=${version} qgis-provider-grass=${version} python3-qgis=${version} python3-qgis-common=${version} libqgis-customwidgets=${version} qgis-providers=${version} qgis-providers-common=${version} qgis-common=${version} \
	libqgis-3d${version_simple} libqgis-core${version_simple} libqgis-analysis${version_simple} libqgis-app${version_simple} libqgis-gui${version_simple} libqgis-native${version_simple} libqgis-server${version_simple} libqgispython${version_simple}
