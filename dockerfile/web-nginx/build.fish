#!/bin/fish

# 接收版本号参数
set image_version $argv[1]

if test -z $image_version
    echo 请指定版本号！
    exit
end

# 打包代码
echo 正在打包代码...
cd ../../PyWPS-frontend
npm run build
tar -cvf ../dockerfile/web-nginx/frontend.tar -C ./dist/ .

# 构建Docker镜像
set image_name swsk33/cloud-geo-nginx
echo 正在构建镜像...
cd ../dockerfile/web-nginx/

# 构建分布式部署用的镜像
echo "Building distributed image..."
docker build --build-arg ALL_PROXY="http://host.docker.internal:7500" -f Dockerfile-distributed -t $image_name:distributed-$image_version .


# 构建单体部署用的镜像
echo "Building single image..."
docker build --build-arg ALL_PROXY="http://host.docker.internal:7500" -f Dockerfile-single -t $image_name:single-$image_version .

# 清理
echo 清理打包...
rm *.tar

echo 构建完成！
