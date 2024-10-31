#!/bin/bash

# 读取环境变量
WORK_DIR=${WORK_DIR:-}
MONGO_HOST=${MONGO_HOST:-}
MONGO_PORT=${MONGO_PORT:-}
MONGO_DB_NAME=${MONGO_DB_NAME:-}
MONGO_USERNAME=${MONGO_USERNAME:-}
MONGO_PASSWORD=${MONGO_PASSWORD:-}
REDIS_HOST=${REDIS_HOST:-}
REDIS_PORT=${REDIS_PORT:-}
REDIS_DB=${REDIS_DB:-}
REDIS_PASSWORD=${REDIS_PASSWORD:-}
CONSUL_IP=${CONSUL_IP:-}
CONSUL_PORT=${CONSUL_PORT:-}
SERVICE_NAME=${SERVICE_NAME:-}
SERVICE_IP=${SERVICE_IP:-}
SERVICE_PORT=${SERVICE_PORT:-}
FILE_SERVER_URL=${FILE_SERVER_URL:-}
DEPLOY_MODE=${DEPLOY_MODE:-}
# uWSGI相关环境变量
UWSGI_PROCESSES=${UWSGI_PROCESSES:-}
UWSGI_THREADS=${UWSGI_THREADS:-}
UWSGI_BUFFER_SIZE=${UWSGI_BUFFER_SIZE:-}

# 构建 pyargv 参数
new_pyargv=""

[ -n "$WORK_DIR" ] && new_pyargv+=" --work_dir $WORK_DIR"
[ -n "$MONGO_HOST" ] && new_pyargv+=" --mongo_host $MONGO_HOST"
[ -n "$MONGO_PORT" ] && new_pyargv+=" --mongo_port $MONGO_PORT"
[ -n "$MONGO_DB_NAME" ] && new_pyargv+=" --mongo_db_name $MONGO_DB_NAME"
[ -n "$MONGO_USERNAME" ] && new_pyargv+=" --mongo_username $MONGO_USERNAME"
[ -n "$MONGO_PASSWORD" ] && new_pyargv+=" --mongo_password $MONGO_PASSWORD"
[ -n "$REDIS_HOST" ] && new_pyargv+=" --redis_host $REDIS_HOST"
[ -n "$REDIS_PORT" ] && new_pyargv+=" --redis_port $REDIS_PORT"
[ -n "$REDIS_DB" ] && new_pyargv+=" --redis_db $REDIS_DB"
[ -n "$REDIS_PASSWORD" ] && new_pyargv+=" --redis_password $REDIS_PASSWORD"
[ -n "$CONSUL_IP" ] && new_pyargv+=" --consul_ip $CONSUL_IP"
[ -n "$CONSUL_PORT" ] && new_pyargv+=" --consul_port $CONSUL_PORT"
[ -n "$SERVICE_NAME" ] && new_pyargv+=" --service_name $SERVICE_NAME"
[ -n "$SERVICE_IP" ] && new_pyargv+=" --service_ip $SERVICE_IP"
[ -n "$SERVICE_PORT" ] && new_pyargv+=" --service_port $SERVICE_PORT"
[ -n "$FILE_SERVER_URL" ] && new_pyargv+=" --file_server_url $FILE_SERVER_URL"
[ -n "$DEPLOY_MODE" ] && new_pyargv+=" --deploy_mode $DEPLOY_MODE"

# 去除开头的空格
new_pyargv=$(echo $new_pyargv | xargs)

# 检查 uwsgi.ini 文件是否存在
if [[ -f /workdir/uwsgi.ini ]]; then
    # 如果存在，使用sed替换原有的pyargv参数或者直接追加参数
    sed -i "/^pyargv =/c\\pyargv = $new_pyargv" /workdir/uwsgi.ini || echo "pyargv = $new_pyargv" >> /workdir/uwsgi.ini
	# 更新或追加uWSGI相关参数
    sed -i "/^processes =/c\\processes = $UWSGI_PROCESSES" /workdir/uwsgi.ini || echo "processes = $UWSGI_PROCESSES" >> /workdir/uwsgi.ini
    sed -i "/^threads =/c\\threads = $UWSGI_THREADS" /workdir/uwsgi.ini || echo "threads = $UWSGI_THREADS" >> /workdir/uwsgi.ini
    sed -i "/^buffer-size =/c\\buffer-size = $UWSGI_BUFFER_SIZE" /workdir/uwsgi.ini || echo "buffer-size = $UWSGI_BUFFER_SIZE" >> /workdir/uwsgi.ini
fi

# 查看配置
cat /workdir/uwsgi.ini

# 定义清理函数，停止 uWSGI 并注销服务
cleanup() {
  echo "Stopping uWSGI..."
  uwsgi --stop /workdir/uwsgi.pid  # 停止 uWSGI，确保路径正确
  
  echo "Deregistering service from Consul..."
  # Consul 注销命令，假设你有服务的 ID
  curl -s -X PUT http://$CONSUL_IP:$CONSUL_PORT/v1/agent/service/deregister/$SERVICE_NAME-$SERVICE_IP-$SERVICE_PORT
}

# 捕获 SIGTERM 信号并调用清理函数
trap cleanup SIGTERM

# 启动 uWSGI 服务并在后台运行
uwsgi --ini /workdir/uwsgi.ini &

# 保存 uWSGI 的进程 ID
UWSGI_PID=$!

# 持续输出日志，同时等待 uWSGI 进程结束
tail -f /workdir/logs/uwsgi.log &

# 等待uWSGI进程，确保清理函数能在接收信号时执行
wait $UWSGI_PID