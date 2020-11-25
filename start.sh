#!/bin/sh
current_path=$(cd $(dirname $0); pwd)
cd ${current_path}
gunicorn --log-level debug kratos.asgi:application -c ./gunicorn_conf.py -D
export PYTHONOPTIMIZE=1;celery -A kratos worker -c `expr 2 \* $([ -f /proc/cpuinfo ] && cat /proc/cpuinfo|grep "physical id"|wc -l || echo 1)`  -l info
