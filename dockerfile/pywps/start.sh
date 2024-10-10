#!/bin/bash

# 拼接 pyargv 参数
PYARGV="${UWSGI_WORK_DIR}"

# 启动uWSGI服务
uwsgi --http $UWSGI_HTTP \
      --chdir $UWSGI_CHDIR \
      --wsgi-file $UWSGI_WSGI_FILE \
      --callable $UWSGI_CALLABLE \
      --processes $UWSGI_PROCESSES \
      --master $UWSGI_MASTER \
      --threads $UWSGI_THREADS \
      --daemonize $UWSGI_DAEMONIZE \
      --pidfile $UWSGI_PIDFILE \
      --buffer-size $UWSGI_BUFFER_SIZE \
      --pyargv "$PYARGV"