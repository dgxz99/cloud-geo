#!/bin/bash
# 删除已存在的 Xvfb 锁文件
if [ -f /tmp/.X99-lock ]; then
	rm /tmp/.X99-lock
fi
# 启动 Xvfb
Xvfb :99 -screen 0 1024x768x24 &
# 等待 Xvfb 启动
sleep 1
# 执行传入的命令
exec "$@"
