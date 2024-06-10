#!/bin/fish
echo 删除缓存...
set cache_list (find ../../pywps-pyqgis/src -type d -name __pycache__)
for cache_dir in $cache_list
    rm -r $cache_dir
    echo 已删除缓存：$cache_dir
end

echo 正在打包代码...
tar -czvf src.tar.gz -C ../../pywps-pyqgis/src .
tar -czvf data.tar.gz -C ../../pywps-pyqgis templates output_map_rule.json process_WPS2.0_description_json pywps.cfg requirements.txt

echo 正在构建镜像...
docker build -f Dockerfile -t pywps-pyqgis:1.0.0 .

echo 清理打包...
rm *.tar.gz

echo 构建完成！
