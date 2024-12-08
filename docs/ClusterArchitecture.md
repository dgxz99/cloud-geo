# CloudGeoPy's distributed online geographic information service

This project realizes publishing a distributed online cloud service (distributed WPS service) for online geographic information processing by using Spring Cloud with WPS-Service to build a cluster.

## 1, Architecture Overview

The overall architecture diagram is shown below:

![image-20241207103512708](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241207103512708.png)

Each part of the above diagram is a separate node as follows:

- `Consul` is the service registry node, which enables multiple clusters of service modules to register to this registry and provides service discovery functionality
- The gateway is a gateway node based on Spring Cloud Gateway, which is located at the outermost layer to receive all user requests. After receiving a request, it can get the cluster information of the registered services from the registry, including all the nodes in a cluster, and then implement load balancing through linear polling to evenly distribute user requests to different nodes in a cluster.
- Each WPS-Service node will provide complete WPS geoprocessing services, they will be automatically registered to the Consul registry at startup, and then receive HTTP requests forwarded by the Gateway, which conform to the OGC WPS specification, and then call the relevant PyQGIS algorithms to complete the data processing.
- The file service node provides API for file uploading and downloading, and can obtain files according to the file direct chain. When the user uploads a file, he/she can obtain the file direct chain and pass the direct chain as an input parameter to the WPS-Service arithmetic operator, and vice versa, when the WPS-Service completes the arithmetic calculations, it will also upload the resultant file to the file service and return the resultant file's direct chain to the user, and all the files are stored in MinIO or MinIO cluster.

## 2, Calling Example

The information of all the nodes deployed in the experimental environment is as follows:

| Docker Container Name | Service                   | Address                    | Port |
| --------------------- | ------------------------- | -------------------------- | ---- |
| consul                | Consul Registry           | 202.114.148.161 (intranet) | 8500 |
| minio                 | MinIO File Object Storage | 202.114.148.161 (intranet) | 9000 |
| redis                 | Redis Cache Server        | 202.114.148.161 (intranet) | 6379 |
| wps-gateway           | Spring Cloud Gateway node | 127.0.0.1                  | 9000 |
| wps-file-storage      | File Service node         | 127.0.0.1                  | 8800 |
| wps-service1          | WPS-Service node 1        | 127.0.0.1                  | 8001 |
| wps-service2          | WPS-Service node 2        | 127.0.0.1                  | 8002 |
| wps-service3          | WPS-Service node 3        | 127.0.0.1                  | 8003 |

The above three `wps-service-n` constitute a complete WPS service cluster, in addition to Redis, MinIO, gateway, file services can also be set up as a cluster if necessary.

### (1) Service Registration

When all the above services are started, the WPS-Service server will automatically register with the Consul registry, there is no need for us to register them manually, you can view all the registered services on the Consul console page (browser access `202.114.148.161:8500`):

![image-20241207104101458](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241207104101458.png)

Entering the service, we can see the full node information in a cluster:

![image-20240606105134191](https://swsk33-note.oss-cn-shanghai.aliyuncs.com/image-20240606105134191.png)

In Spring Boot, just integrate Consul Starter and configure it to automatically register services into Consul at startup, and in WPS-Service, integrate `py-consul` to realize registering services into Consul:

```python
import os
from config import get_config
from consul import Consul

config = get_config()

# Consul address and port
consul_host = config.get("consul", "consul_ip")
consul_port = config.getint("consul", "consul_port")

# Globally unique Consul client object
consul_client = Consul(host=consul_host, port=consul_port)


# Registration Services
def register_consul(service_name, service_address, service_port):
	# Service ID, which should be unique per node
	service_id = f'{service_name}-{service_address}-{service_port}'
	# register services
	consul_client.agent.service.register(
		service_id=service_id,
		name=service_name,
		address=service_address,
		port=service_port,
		check={
			'http': f'http://{service_address}:{service_port}/health',
             'method': 'get',
			'interval': '10s',
			'timeout': '1s',
		})


# deregistration node
def deregister_consul(service_name, service_address, service_port):
	service_id = f'{service_name}-{service_address}-{service_port}'
	consul_client.agent.service.deregister(service_id)
```

然后在入口文件中完成启动时的注册和退出应用程序时自动注销：

```python
# Register to Consul
register_consul(service_name, service_ip, service_port)
# Automatic service logout on server shutdown
atexit.register(deregister_consul, service_name, service_ip, service_port)
```

### (2) Interface Description

All requests are forwarded through the gateway, and different path prefixes are able to route to different services. The address of the gateway when deployed locally is `127.0.0.1:9000`, and all the API paths are described below, where `{}` surrounded by denotes parameters.

The first is the WPS-Service service, which is prefixed with `/api/wps`, followed by the path and its request method, all of which conform to the WPS standard:

- The `/api/wps/processes` GET request for information about the full set of operators is the WPS GetCapabilities operation
- `/api/wps/processes/{identifier}` GET request, get a specific operator information, including operator parameters and so on, is the WPS DescribeProcess operation.
- `/api/wps/jobs` POST request, call the execution of an operator, the request body needs to conform to the specification in WPS Execute.
- `/api/wps/jobs/{job-id}` GET request to get the status or execution result of an asynchronously executed operator.

Then there is the file service:

- `/api/file/upload` PUT request to upload a file, successful upload returns information about the uploaded file, including the file `id` and extension, where the name of the file will be auto-generated after uploading
- `/upload-force-name/{name}` PUT request, upload a file, specify the name of the uploaded file.
- `/api/delete/{id}` DELETE request, delete the uploaded file, specify the `id` of the file.
- `/api/find/{id}` GET request, query the metadata of a file, specify the file `id`.
- `/api/retrieve/{name}` GET request to download a file, specifying the full name of the file in the form `id.extension`

The configuration file for the gateway is as follows:

```yaml
server:
  port: 9000

spring:
  application:
    name: "wps-gateway"
  codec:
    max-in-memory-size: 1024MB
  servlet:
    multipart:
      max-file-size: 1024MB
      max-request-size: 1024MB
  cloud:
    consul:
      host: "202.114.148.161"
      port: 8500
      discovery:
        service-name: ${spring.application.name}
        instance-id: ${spring.application.name}-${spring.cloud.client.hostname}-${server.port}
        prefer-ip-address: true
        heartbeat:
          enabled: true
    gateway:
      discovery:
        locator:
          enabled: true
      routes:
        # WPS Service
        - id: "py-wps"
          uri: "lb://py-wps"
          predicates:
            - "Path=/api/wps/**"
          filters:
            - RewritePath=/api/wps/(?<remaining>.*), /${remaining}
        # Distributed file service
        - id: "file-upload"
          uri: "lb://wps-file-storage"
          predicates:
            - "Path=/api/file/**"
```

### (3) Invoking service-synchronization mode

The user needs to use an OGC WPS compliant HTTP request to invoke the corresponding operator by simply sending a POST request to the **Gateway**.

First the user needs to upload the input file to the file service API, suppose there is an existing `point.zip` file, which is a Shapefile compressed package of point data, then the user needs to launch a PUT request to `127.0.0.1:9000/api/file/upload`, the request body is in the form of `form-data` and only The request body is in the form of `form-data`, which only contains the file entry to be uploaded, the `key` is specified as `file`, and the `value` is specified as the file to be uploaded, `point.zip`, and the upload succeeds to get the result as follows:

```json
{
    "message": "上传文件完成！",
    "success": true,
    "data": {
        "name": "7c4a5e4e6b844d0aa27dfaaf27b4dbf1",
        "format": "tif",
        "length": 27567495,
        "objectName": "7c4a5e4e6b844d0aa27dfaaf27b4dbf1",
        "etag": "\"a623c694c4e4fbffac79ccda5d05fe52-6\""
    }
}
```

The above `data` field is the actual uploaded file information, where:

- `name` indicates the `id` of the uploaded file
- `format` the extension of the file

At this point, the user can get the direct link to the uploaded file: `http://127.0.0.1:9000/api/file/retrieve/7c4a5e4e6b844d0aa27dfaaf27b4dbf1.tif`.

Then call the corresponding WPS service to launch a POST request to address `127.0.0.1:9000/api/wps/jobs`, and use our file direct link as the parameter input, the content of the request body example:

```json
{
    "identifier": "otb:BandMath",
    "inputs": {
        "il": {
            "type": "reference",
            "href": "http://127.0.0.1:9000/api/file/retrieve/7c4a5e4e6b844d0aa27dfaaf27b4dbf1.tif"
        },
        "exp": "(im1b4 - im1b3) / (im1b4 + im1b3)"
    }
}
```

The request invokes an operator for OTB band calculations with all default parameters, and specific data is passed by specifying a direct link to the file URL.

If the operator executes properly, the result of the operator execution is obtained as a response:

```json
{
    "success": true,
    "msg": "success",
    "data": {
        "jobId": "5a50bceebfb44bbaaee229af78cfa0bf",
        "status": "succeeded",
        "completionTime": "2024-12-03 19:03:57.201",
        "expirationTime": "2024-12-04 19:03:57.201",
        "percentCompleted": "100",
        "message": "WPS-Service Process BandMath finished",
        "output": {
            "out": "http://localhost:5000/outputs/otb-BandMath-out-c13a2fde-16ba-4777-9fde-55e62ff72e47.tif"
        }
    }
}
```

Each WPS-Service publishes all QGIS operators, i.e., each caller node publishes the complete WPS service, and the user can specify the operator to be called by using the `identifier` field when calling via a request from the WPS specification. You can also view the parameter structure of the corresponding operator by viewing the details of all operators or one operator through the corresponding API before calling.

In addition, the result file obtained by WPS when running the operator is also uploaded to the file server and returned as a direct link.

Here, `12` threads are used, each thread initiates `3` requests to simulate concurrent access, and then the gateway spreads all the requests to the three different caller nodes mentioned above to achieve load balancing.

It should be noted that this is a synchronous call, so after each request is made, the request will hang until the operator has finished processing and calculating and returned the result, for more complex operators with long processing times, it is recommended to use the asynchronous call mode.

### (4) Calling a service - asynchronous mode

In the WPS 2.0 standard, the asynchronous calling mode has been added. For some very complicated processing tasks, the server side may need a very long time to complete, then we need to use the asynchronous calling mode to execute an operator. When calling an operator asynchronously, the server will execute the operator in the background, and then the user can use the `GetStatus` and `GetResult` operations to The user can then query whether the call has finished by using the `GetStatus` and `GetResult` operations.

![image-20240607202056908](https://swsk33-note.oss-cn-shanghai.aliyuncs.com/image-20240607202056908.png)

However, in distributed scenarios, WPS-Service is deployed in clusters, and users may request to different nodes each time. Therefore, if the default way is to store the JobId locally in the node, it may lead to the problem of not being able to find the process in the subsequent GetStatus.

Therefore, the Redis database is introduced here, all the process IDs, execution status, results and other information of the asynchronous execution of the operator will be stored in the Redis database and synchronized in real time, and the user can also get the execution status and results of the operator through the corresponding interface, and the WPS-Service also gets them from Redis, so that there is no need to care about which node the user's request has been forwarded to. In this way, it doesn't need to care about which node the user's request is forwarded to, and the process status and results are uniformly obtained from Redis.

When making asynchronous calls, you need to set the `mode` field in the request body to `async` as follows:

```json
{
    "identifier": "otb:BandMath",
    "mode": "async",
    "inputs": {
        "il": {
            "type": "reference",
            "href": "http://127.0.0.1:9000/api/file/retrieve/7c4a5e4e6b844d0aa27dfaaf27b4dbf1.tif"
        },
        "exp": "(im1b4 - im1b3) / (im1b4 + im1b3)"
    }
}
```

At this point, the WPS server does not return the result immediately, but returns a JobId:

```json
{
  "success": true,
  "msg": "success",
  "data": {
    "JobId": "53972f2eaffc4a92916aa604b9504625",
    "status": "Running",
    "result": null
  }
}
```

To get the operator execution status or result, the user can make a query using the above JobId and make a GET request to `http://127.0.0.1:9000/api/wps/job/53972f2eaffc4a92916aa604b9504625` with the following result:

```json
{
  "success": true,
  "msg": "success",
  "data": {
    "JobId": "53972f2eaffc4a92916aa604b9504625",
    "status": "succeeded",
    "result": {
      "completionTime": "2024-12-03 19:04:19.936",
      "expirationTime": "2024-12-04 19:04:19.936",
      "percentCompleted": "100",
      "message": "WPS-Service Process BandMath finished",
      "output": {
        "out": "http://localhost:5000/outputs/otb-BandMath-out-cbb612a9-576a-4770-ad1f-17e4280e811c.tif"
      }
    }
  }
}
```

It can be seen that the `status` field is `Succeeded` and contains the `result` field, indicating that the operator has been executed asynchronously and a result has been obtained.

## 3, WPS-Service and PyQGIS Related Introduction

**WPS-Service** in the main use of the PyWPS framework, PyWPS is the OGC Web Processing Service (**OGC ** **WPS **) standard server-side implementation of the use of **Python ** programming language.

The official documentation is located at https://WPS-Service.readthedocs.io/en/latest/index.html

The use of PyWPS server-side, you need to combine the use of python web framework, combined with the official case, choose to use the flask framework, the use of the framework to create API interfaces, to facilitate the user to directly call the PyWPS service. Roughly the process is shown in the following figure:

![image-20241207105256146](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241207105256146.png)

When the process is registered, here in the PyWPS service, the processing of the process will be carried out, such as: turning into the corresponding PyWPS description of the standard information; when the user calls the operator, it will be carried out in the input file checksum, the execution of the operator, the output file results and so on. As long as the process is successfully injected, PyWPS will automatically process some operations.

In QGIS provides a lot of open-source operators, so the open-source operators in PyQGIS will be converted into the process in PyWPS to realize the online processing of geographic data.

![image-20241207105800914](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241207105800914.png)

Unified access to third-party operators through PyQGIS.

![image-20241203193537254](https://dg-typora.oss-cn-chengdu.aliyuncs.com/image-20241203193537254.png)

