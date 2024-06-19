#!/bin/fish

set image_version $argv[1]

if test -z $image_version
    echo 请指定版本号！
    exit
end

echo 正在构建镜像...
docker build --network host --build-arg ALL_PROXY="http://127.0.0.1:7500" -f Dockerfile -t swsk33/op-gis-environment:$image_version .
echo 构建完成！
