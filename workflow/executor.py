import os
from datetime import datetime
from .utils import env as ENV
from .utils.logger import Logger
from kratos.apps.log.serializers import LogSerializer
from kratos.apps.log.models import Log
from .tasks import *

def run(pipeline, envs = {}):
    
    ENV._init(envs)

    ENV.SET('name', pipeline['appinfo']['name'])
    ENV.SET('app_id', pipeline['appinfo']['id'])
    
    # 新建日志记录
    serializer = LogSerializer(data={'pipeline': pipeline['id'], 'status': 0})
    serializer.is_valid(raise_exception=True)
    log_instance = serializer.save()
    
    # 配置logger
    logger = Logger()
    logger.add_file_handler(path=serializer.data['path'])
    logger = logger.logger
    ENV.SET('logger', logger)
    
    for task in pipeline['tasks']:
        getattr(globals()[task['name']], task['name'])(**task['params']).exec()
    
    # 日志状态更新
    complete_at = datetime.now()
    create_at = datetime.strptime(str(log_instance.created_at), "%Y-%m-%d %H:%M:%S.%f")
    duration = (complete_at - create_at).seconds
    log_instance.duration = duration
    log_instance.status = 1
    log_instance.save()

    return log_instance.id
