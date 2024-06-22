#!/bin/fish

# 接收版本号参数
set image_version $argv[1]

if test -z $image_version
    echo 请指定版本号！
    exit
end

# 构建后端代码
echo 构建后端...
cd ../../server-springcloud
mvn clean package
cp ./gateway/target/*.jar ../dockerfile/springcloud/gateway/gateway.jar
cp ./file-storage/target/*.jar ../dockerfile/springcloud/file/file.jar

# 构建Docker镜像
set gateway_image_name swsk33/distribute-geoprocessing-gateway
set file_image_name swsk33/distribute-geoprocessing-file

echo 构建镜像...
cd ../dockerfile/springcloud
docker build -f ./gateway/Dockerfile -t $gateway_image_name:$image_version ./gateway
docker build -f ./file/Dockerfile -t $file_image_name:$image_version ./file

echo 创建latest tag...
docker tag $gateway_image_name:$image_version $gateway_image_name
docker tag $file_image_name:$image_version $file_image_name

# 清理
echo 清理构建...
rm ./gateway/*.jar
rm ./file/*.jar

echo 构建完成！
