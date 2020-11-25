from .base import *

DEBUG = True

# ----------公共数据库配置----------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ktsdb',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# celery配置
CELERY_BROKER_URL = 'redis://127.0.0.1'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERYD_MAX_TASKS_PER_CHILD = 200
CELERY_WORKER_CONCURRENCY = 4
CELERY_TASK_RESULT_EXPIRES = 864000
