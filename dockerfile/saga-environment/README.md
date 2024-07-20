# SAGA-GIS算子环境

一个SAGA GIS算子环境镜像，基于Ubuntu 22.04 (jammy)版本制作，其中编译时已加入全部可选功能。

## 使用方法

### (1) 创建数据卷

可以先创建数据卷并将相应的数据存放到数据卷：

```bash
docker volume create saga-data
```

### (2) 创建容器

创建容器时挂载数据卷，进入容器的`bash`终端并通过命令行调用`saga_cmd`即可：

```bash
# 创建容器
docker run -it --name saga-gis -v saga-data:/data swsk33/saga-gis-environment bash
# 调用命令
saga_cmd -h
```

后续调用`saga_cmd`调用算子即可。
