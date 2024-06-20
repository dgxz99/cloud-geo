FROM ubuntu:jammy
# 准备环境
ADD install-qgis-ubuntu.sh /
ADD pre-start.sh /
# 环境变量
ENV PYTHONPATH=/usr/share/qgis/python/plugins
ENV PATH=/opt/otb/bin:$PATH
ENV DISPLAY=:99
# 配置环境
RUN apt update \
	# 安装证书
	&& apt install -y ca-certificates \
	# 替换软件源
	&& echo "deb https://mirror.tuna.tsinghua.edu.cn/ubuntu jammy main multiverse restricted universe" > /etc/apt/sources.list \
	&& echo "deb https://mirror.tuna.tsinghua.edu.cn/ubuntu jammy-backports main multiverse restricted universe" >> /etc/apt/sources.list \
	&& echo "deb https://mirror.tuna.tsinghua.edu.cn/ubuntu jammy-proposed main multiverse restricted universe" >> /etc/apt/sources.list \
	&& echo "deb https://mirror.tuna.tsinghua.edu.cn/ubuntu jammy-security main multiverse restricted universe" >> /etc/apt/sources.list \
	&& echo "deb https://mirror.tuna.tsinghua.edu.cn/ubuntu jammy-updates main multiverse restricted universe" >> /etc/apt/sources.list \
	&& apt update \
	&& apt full-upgrade -y \
	# 安装相关工具和依赖
	&& apt install -y gnupg software-properties-common vim wget xvfb saga \
	# 添加QGIS软件源
	&& wget -O /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg \
	&& echo "Types: deb" > /etc/apt/sources.list.d/qgis.sources \
	&& echo "URIs: https://qgis.org/ubuntu-ltr" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Suites: jammy" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Architectures: amd64" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Components: main" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Signed-By: /etc/apt/keyrings/qgis-archive-keyring.gpg" >> /etc/apt/sources.list.d/qgis.sources \
	&& apt update \
	# 安装QGIS
	&& chmod +x install-qgis-ubuntu.sh \
	&& /install-qgis-ubuntu.sh \
	# 下载OTB
	&& mkdir -p /opt/otb \
	&& wget -O /otb.tar.gz https://www.orfeo-toolbox.org/packages/OTB-9.0.0-Linux.tar.gz \
	&& tar -xzvf /otb.tar.gz -C /opt/otb \
	# 清理
	&& apt autoremove -y \
	&& apt clean \
	&& rm -rf /otb.tar.gz /var/lib/apt/lists/* /install-qgis-ubuntu.sh \
	# 准备
	&& chmod +x /pre-start.sh
ENTRYPOINT ["/pre-start.sh"]
CMD ["bash"]