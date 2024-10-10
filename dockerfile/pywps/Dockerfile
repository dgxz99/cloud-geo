FROM swsk33/op-gis-environment
# 准备环境
ADD src.tar.gz /server
ADD data.tar.gz /workdir
ADD start.sh /workdir/
# 工作目录
WORKDIR /workdir
# 配置环境
RUN apt update \
	&& apt install -y python3-pip \
	&& apt clean \
	&& rm -rf /var/lib/apt/lists/* \
	&& pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
	&& pip install -r requirements.txt \
	&& chmod +x start.sh

# 设置环境变量
ENV UWSGI_HTTP=0.0.0.0:5000
ENV UWSGI_CHDIR=/server/src
ENV UWSGI_WSGI_FILE=/server/src/manage.py
ENV UWSGI_CALLABLE=app
ENV UWSGI_PROCESSES=2
ENV UWSGI_MASTER="true"
ENV UWSGI_THREADS=2
ENV UWSGI_DAEMONIZE="./logs/uwsgi.log"
ENV UWSGI_PIDFILE=uwsgi.pid
ENV UWSGI_BUFFER_SIZE=32768
ENV UWSGI_WORK_DIR="--work_dir /workdir"

# 端口
EXPOSE 5000
# 数据卷
VOLUME ["/workdir"]
# CMD ["/workdir/start.sh"]