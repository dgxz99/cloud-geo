FROM swsk33/op-gis-environment
# 准备环境
ADD src.tar.gz /server
ADD data.tar.gz /workdir
ADD start.sh /workdir
# 工作目录
WORKDIR /workdir
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