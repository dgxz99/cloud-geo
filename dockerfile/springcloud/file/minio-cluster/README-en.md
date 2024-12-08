## 1. docker deploy minio cluster

Pull the minio image:

```bash
docker pull minio/minio
```

Deploy a Minio cluster containing four nodes using docker compose to orchestrate containers.

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

Caution:

- **On the same host**, ensure that each container is on the **same network**.
- The **user and password for each node needs to be the same**.

Under this `docker-compose.yml` path, run the following command to start the 4 containers:

```bash
docker compose up -d
```

Then visit `http://127.0.0.1/9001` to log into the console and view the Minio node information. Use the settings `MINIO_ROOT_USER` and `MINIO_ROOT_PASSWORD` to log in.

![image-20241029152153971](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029152153971.png)

View all node information.

![image-20241029152349182](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029152349182.png)

Caution:

- If deployed on different servers, each container needs to be mapped with a corresponding port, and then the service with the corresponding ip address (http://<minio_host>:<minio_port>/data) needs to be run at startup.

## 2. Minio cluster test

Create a bucket, here the name (customizable) is set to: wps-file, and then upload a file, e.g. Landsat_wh.tif

![image-20241029153100538](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029153100538.png)

The easiest way to see if each node is storing a portion of the data is to see if that portion exists in all of the data volumes corresponding to the Minio container:

![image-20241029153800374](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029153800374.png)

Now let's stop both nodes and check that is both have normal access to the data:
![image-20241029154002418](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154002418.png)

![image-20241029154039113](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154039113.png)

You can still access the downloaded data normally, and after downloading the data to view and did not lose part of the data, normal display.

When stopping another node, view it again:

![image-20241029154304216](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154304216.png)

![image-20241029154347471](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241029154347471.png)

Here it is found that there is no data in the bucket and the data is not accessible at this point. If the container is restarted and it is found that the data is still accessible, then it means that the data in the Minio cluster can be accessed as long as half of the nodes are guaranteed to be up and running.