# SAGA-GIS算子环境

一个SAGA GIS算子环境镜像，基于Ubuntu 22.04 (jammy)版本制作，其中编译时已加入全部可选功能。

## 使用方法

拉取镜像后，进入容器的`bash`终端并通过命令行调用`saga_cmd`即可：

```bash
# 创建容器
docker run -it --name saga-gis swsk33/saga-gis-environment bash
# 调用命令
saga_cmd -h
```
