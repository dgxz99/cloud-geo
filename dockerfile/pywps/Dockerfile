FROM swsk33/op-gis-environment
# 准备环境
ADD src.tar.gz /server
ADD data.tar.gz /workdir
ADD start.sh /workdir
# 工作目录
WORKDIR /workdir
# 项目运行环境变量
ENV WORK_DIR=/workdir
ENV MONGO_HOST=127.0.0.1
ENV MONGO_PORT=27017
ENV MONGO_DB_NAME=pywps
ENV MONGO_USERNAME=''
ENV MONGO_PASSWORD=''
ENV REDIS_HOST=127.0.0.1
ENV REDIS_PORT=6379
ENV REDIS_DB=0
ENV REDIS_PASSWORD=''
ENV CONSUL_IP=127.0.0.1
ENV CONSUL_PORT=8500
ENV SERVICE_NAME=py-wps
ENV SERVICE_IP=127.0.0.1
ENV SERVICE_PORT=5000
ENV FILE_SERVER_URL=''
ENV DEPLOY_MODE=single
# uWSGI环境变量
ENV UWSGI_PROCESSES=2
ENV UWSGI_THREADS=2
ENV UWSGI_BUFFER_SIZE=32768
# 配置环境
RUN apt update \
	&& apt install -y python3-pip \
	&& apt clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
	&& pip install -r requirements.txt \
	&& pip install uwsgi \
	&& mkdir /workdir/logs \
	&& touch /workdir/logs/uwsgi.log \
	&& chmod +x start.sh

# 端口
EXPOSE 5000
# 数据卷
VOLUME ["/workdir"]
CMD ["./start.sh"]