## 1、docker部署Minio集群

拉取minio镜像：

```bash
docker pull minio/minio
```

利用docker compose编排容器，部署含有四个节点的Minio集群。

```yaml
version: '3.8'

services:
    minio1:
        image: minio/minio
        container_name: minio1
        environment:
            - MINIO_ROOT_USER=admin
            - MINIO_ROOT_PASSWORD=12345678
        volumes:
            - minio-data1:/data
        ports:
            - "9000:9000"
            - "9001:9001"
        command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"
        networks:
            - minio-net

    minio2:
        image: minio/minio
        container_name: minio2
        environment:
            - MINIO_ROOT_USER=admin
            - MINIO_ROOT_PASSWORD=12345678
        volumes:
            - minio-data2:/data
        command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"
        networks:
            - minio-net

    minio3:
        image: minio/minio
        container_name: minio3
        environment:
            - MINIO_ROOT_USER=admin
            - MINIO_ROOT_PASSWORD=12345678
        volumes:
            - minio-data3:/data
        command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"
        networks:
            - minio-net

    minio4:
        image: minio/minio
        container_name: minio4
        environment:
            - MINIO_ROOT_USER=admin
            - MINIO_ROOT_PASSWORD=12345678
        volumes:
            - minio-data4:/data
        command: server http://minio1/data http://minio2/data http://minio3/data http://minio4/data --console-address ":9001"
        networks:
            - minio-net

volumes:
    minio-data1:
    minio-data2:
    minio-data3:
    minio-data4:


networks:
    minio-net:
        driver: bridge

```

注意：

- **同一宿主机**上，保证每个容器在**同一网络**下。
- 每一个节点的**用户与密码需要保持一致**。

在这个`docker-compose.yml`路径下，运行如下命令，启动4个容器：
```bash
docker compose up -d
```

然后访问`http://127.0.0.1/9001`就可以登录控制台，查看Minio节点信息。使用设置的`MINIO_ROOT_USER`与`MINIO_ROOT_PASSWORD`进行登录。

![image-20241029152153971](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029152153971.png)

查看所有节点信息。

![image-20241029152349182](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029152349182.png)

注意：

- 若是在不同的服务器上部署，每一个容器都需要映射对应的端口，然后在启动时，需要运行对应的ip地址（http://<minio_host>:<minio_port>/data）的服务。

## 2、Minio集群测试

创建一个桶，这里名称（可自定义）设为：wps-file，然后上传一个文件，如：Landsat_wh.tif

![image-20241029153100538](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029153100538.png)

如何查看是否每个节点都存储了部分数据，最简单的方法就是查看Minio容器对应的数据卷中是否都存在这一份数据：

![image-20241029153800374](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029153800374.png)

现在我们停止两个节点，查看是都可以正常访问数据：
![image-20241029154002418](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154002418.png)

![image-20241029154039113](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154039113.png)

还是可以正常访问下载数据的，并且下载数据后查看并没有丢失部分数据，正常显示。

当再停止一个节点时，再次查看：

![image-20241029154304216](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154304216.png)

![image-20241029154347471](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154347471.png)

这里发现桶里是没有数据的，此时的数据不可以访问。若重新启动容器，发现数据仍可以访问，则就是只要保证有一半的节点是正常运行的，就可以访问Minio集群中的数据。