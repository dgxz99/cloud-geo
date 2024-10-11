#!/bin/bash

# 将系统的gdal提前，默认使用系统的gdal
export PATH=/usr/bin:$PATH

# 启动 uWSGI 服务
uwsgi --ini /workdir/uwsgi.ini
# 查看输出日志
tail -f /workdir/logs/uwsgi.log