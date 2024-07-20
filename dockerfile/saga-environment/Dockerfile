FROM ubuntu:jammy
# 环境变量
ENV DEBIAN_FRONTEND=noninteractive
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
	&& apt install -y wget \
	&& wget -O /usr/share/keyrings/codelite-archive-keyring.asc https://repos.codelite.org/CodeLite.asc \
	&& echo "deb [signed-by=/usr/share/keyrings/codelite-archive-keyring.asc] https://repos.codelite.org/wx3.2/ubuntu jammy universe" >/etc/apt/sources.list.d/codelite.list \
	&& apt update -y \
	&& apt install -y libtiff5-dev libgdal-dev libproj-dev libexpat1-dev libogdi-dev unixodbc-dev \
	libwxbase3.2-0-unofficial libwxbase3.2unofficial-dev libwxgtk3.2-0-unofficial libwxgtk3.2unofficial-dev wx3.2-headers wx-common \
	libomp-dev libqhull-dev libhpdf-dev libopencv-dev libsvm-dev libpdal-dev libcurl4-openssl-dev libgeotranz3-dev python3 swig libnotify-dev \
	g++ cmake cmake-qt-gui make libtool git \
	# 下载SAGA源码
	&& mkdir /saga-build \
	&& cd /saga-build \
	&& wget -O saga.tar.gz "https://liquidtelecom.dl.sourceforge.net/project/saga-gis/SAGA%20-%209/SAGA%20-%209.5.1/saga-9.5.1.tar.gz" \
	&& tar -xzvf saga.tar.gz \
	&& cd saga-9.5.1 \
	&& mkdir build \
	&& cd build \
	# 开始编译
	&& cmake ../saga-gis -DCMAKE_BUILD_TYPE=RELEASE -DWITH_TRIANGLE=OFF -DWITH_SYSTEM_SVM=ON -DWITH_DEV_TOOLS=OFF \
	&& cmake --build . --config Release -j 16 \
	&& cmake --install . \
	&& ldconfig \
	# 清理
	&& apt purge -y wget g++ cmake cmake-qt-gui make libtool git \
	&& apt autoremove -y \
	&& apt clean \
	&& rm -rf /saga-build /var/lib/apt/lists/*
# 数据卷
VOLUME ["/data"]
# 工作目录
WORKDIR /data
CMD ["bash"]