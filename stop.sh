#!/bin/sh
kill -9 `ps aux |grep gunicorn |grep kratos.asgi | awk '{ print $2 }'`
ps auxww|grep "celery worker"|grep -v grep|awk '{print $2}'|xargs kill -9       # 关闭所有celery进程
