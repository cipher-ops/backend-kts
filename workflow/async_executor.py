import os, time

from celery.app.task import Task
from celery import shared_task
from celery.result import AsyncResult

from datetime import datetime

from kratos.apps.log.serializers import LogSerializer
from kratos.apps.log.models import Log

from .utils import env as ENV
from .utils.logger import Logger
from .tasks import *

class CallbackTask(Task):
    def __init__(self):
        super(CallbackTask, self).__init__()

    def on_success(self, retval, task_id, args, kwargs):
        logger = Log.objects.get(pk=retval)

        complete_at = datetime.now()
        create_at = datetime.strptime(str(logger.created_at), "%Y-%m-%d %H:%M:%S.%f")
        duration = (complete_at - create_at).seconds

        # 日志状态更新
        logger.duration = duration
        logger.status = 1
        logger.save()

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

@shared_task
def task_add():
    print('before--')
    print("Start : %s" % time.ctime())
    time.sleep(5)
    print('after--')
    print("Start : %s" % time.ctime())
    return 3+2


@shared_task(base=CallbackTask)
def async_run(pipeline, logid, envs = {},):
    # 初始化环境变量
    ENV._init(envs)
    ENV.SET('name', pipeline['appinfo']['name'])
    ENV.SET('app_id', pipeline['appinfo']['id'])
    
    log_instance = Log.objects.get(pk=logid)
    serializer = LogSerializer(log_instance)

    # 配置logger
    logger = Logger()
    logger.add_file_handler(path=serializer.data['path'])
    logger = logger.logger
    ENV.SET('logger', logger)

    # 执行任务流
    for task in pipeline['tasks']:
        getattr(globals()[task['name']], task['name'])(**task['params']).exec()

    return logid
