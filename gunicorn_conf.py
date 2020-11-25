import os, multiprocessing

bind = '0.0.0.0:8009'

# gunicorn worker ：进程数 线程数 允许挂起的链接数
workers = multiprocessing.cpu_count() * 2 + 1
threads = multiprocessing.cpu_count() * 2
backlog = 2048
timeout = 60*60*10
# gunicorn worker class
worker_class = "uvicorn.workers.UvicornWorker"
debug = True

# log
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
errorlog = os.path.join(PROJECT_PATH, "logs/gunicorn_error.log")
accesslog = os.path.join(PROJECT_PATH, 'logs/gunicorn_access.log')
loglevel = "info"
proc_name = 'gunicorn_kts'
default_proc_name = 'gunicorn_kts'
