#!/bin/fish

# 接收版本号参数
set image_version $argv[1]

if test -z $image_version
    echo 请指定版本号！
    exit
end

# 清理Python缓存
echo 删除缓存...
set cache_list (find ../../pywps-pyqgis/src -type d -name __pycache__)
for cache_dir in $cache_list
    rm -r $cache_dir
    echo 已删除缓存：$cache_dir
end

# 打包代码
echo 正在打包代码...
tar -czvf src.tar.gz -C ../../pywps-pyqgis/src .
tar -czvf data.tar.gz -C ../../pywps-pyqgis pywps.cfg requirements.txt uwsgi.ini

# 构建Docker镜像
set image_name swsk33/cloud-geo-py
echo 正在构建镜像...
docker build -f Dockerfile -t $image_name:$image_version .
echo 创建latest tag...
docker tag $image_name:$image_version $image_name

# 清理
echo 清理打包...
rm *.tar.gz

echo 构建完成！
