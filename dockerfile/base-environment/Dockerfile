FROM debian
# 准备环境
ADD install-qgis.sh /
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
	&& rm /etc/apt/sources.list.d/* \
	&& echo "deb https://mirrors.ustc.edu.cn/debian bookworm main non-free non-free-firmware contrib" > /etc/apt/sources.list \
	&& echo "deb https://mirrors.ustc.edu.cn/debian bookworm-updates main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
	&& echo "deb https://mirrors.ustc.edu.cn/debian bookworm-proposed-updates main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
	&& echo "deb https://mirrors.ustc.edu.cn/debian bookworm-backports main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
	&& echo "deb https://mirrors.ustc.edu.cn/debian bookworm-backports-sloppy main non-free non-free-firmware contrib" >> /etc/apt/sources.list \
	&& apt update \
	&& apt full-upgrade -y \
	# 内置常用工具
	&& apt install -y gnupg software-properties-common vim wget xvfb \
	# OTB所需工具
	curl python3 python3-dev python3-numpy make cmake gcc g++ swig findutils file \
	# Saga工具
	saga \
	# 添加QGIS软件源
	&& wget -O /etc/apt/keyrings/qgis-archive-keyring.gpg https://download.qgis.org/downloads/qgis-archive-keyring.gpg \
	&& echo "Types: deb deb-src" > /etc/apt/sources.list.d/qgis.sources \
	&& echo "URIs: https://qgis.org/debian-ltr" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Suites: bookworm" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Architectures: amd64" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Components: main" >> /etc/apt/sources.list.d/qgis.sources \
	&& echo "Signed-By: /etc/apt/keyrings/qgis-archive-keyring.gpg" >> /etc/apt/sources.list.d/qgis.sources \
	&& apt update \
	# 安装QGIS
	&& chmod +x install-qgis.sh \
	&& /install-qgis.sh \
	# 下载OTB
	&& mkdir -p /opt/otb \
	&& wget -O /otb.tar.gz https://www.orfeo-toolbox.org/packages/OTB-9.0.0-Linux.tar.gz \
	&& tar -xzvf /otb.tar.gz -C /opt/otb \
	# 清理
	&& apt autoremove -y \
	&& apt clean \
	&& rm -rf /otb.tar.gz /var/lib/apt/lists/* /install-qgis.sh \
	# 准备
	&& chmod +x /pre-start.sh
ENTRYPOINT ["/pre-start.sh"]
CMD ["bash"]