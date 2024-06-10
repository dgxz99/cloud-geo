FROM debian:bookworm-slim
# 准备环境
ADD sources.list /
ADD qgis.sources /
ADD qgis-archive-keyring.gpg /etc/apt/keyrings/qgis-archive-keyring.gpg
ADD src.tar.gz /server
ADD data.tar.gz /workdir
ADD install-qgis.sh /workdir/install-qgis.sh
# 工作目录
WORKDIR /workdir
# 配置环境
RUN rm /etc/apt/sources.list.d/* &&\
	mv /sources.list /etc/apt/ &&\
	apt update &&\
	apt install -y gnupg software-properties-common ca-certificates python3-pip &&\
	mv /qgis.sources /etc/apt/sources.list.d/ &&\
	apt update &&\
	chmod +x install-qgis.sh &&\
	./install-qgis.sh &&\
	apt clean &&\
	pip install --break-system-packages -r requirements.txt
# 端口
EXPOSE 5000
# 数据卷
VOLUME ["/workdir"]
CMD ["python3", "/server/main.py"]