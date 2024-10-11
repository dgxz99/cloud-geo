#!/bin/fish

# 接收版本号参数
set image_version $argv[1]

if test -z $image_version
    echo 请指定版本号！
    exit
end

# 构建镜像
set image_name swsk33/op-gis-environment
echo 正在构建镜像...
docker build --network host --build-arg ALL_PROXY="http://127.0.0.1:7500" -f Dockerfile -t $image_name:$image_version .
echo 创建latest tag...
docker tag $image_name:$image_version $image_name

echo 构建完成！
