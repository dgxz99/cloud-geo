#!/bin/fish

echo 构建后端...
cd ../../server-springcloud
mvn clean package
cp ./gateway/target/*.jar ../dockerfile/springcloud/gateway/gateway.jar
cp ./file-storage/target/*.jar ../dockerfile/springcloud/file/file.jar

echo 构建镜像...
cd ../dockerfile/springcloud
docker build -f ./gateway/Dockerfile -t wps-gateway:1.0.0 ./gateway
docker build -f ./file/Dockerfile -t wps-file:1.0.0 ./file

echo 清理构建...
rm ./gateway/*.jar
rm ./file/*.jar

echo 构建完成！
