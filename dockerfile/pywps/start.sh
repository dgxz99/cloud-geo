#!/bin/bash

# 启动 uWSGI 服务
uwsgi --ini /workdir/uwsgi.ini
# 查看输出日志
tail -f /workdir/logs/uwsgi.log