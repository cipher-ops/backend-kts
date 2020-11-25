import logging
from colorlog import ColoredFormatter

class Logger(object):
    __instance = None

    # 重写new方法实现单例模式
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            obj = object.__new__(cls)
            cls.__instance = obj
        return cls.__instance

    def __init__(self, level=logging.DEBUG):
        # 如果之前没创建过 就新建一个logger对象，后面相同的实例共用一个logger对象
        if 'logger' not in self.__dict__:
            logger = logging.getLogger('kts-task')
            logger.setLevel(level)

            handler = logging.StreamHandler()
            formatter = ColoredFormatter(
                fmt="%(log_color)s%(asctime)s %(log_color)s%(pathname)s %(log_color)s%(funcName)s [line:%(log_color)s%(lineno)d] %(log_color)s%(levelname)s %(log_color)s%(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

            self.logger = logger

    def add_file_handler(self, path='logs/demo.log'):
        self.logger.addHandler(logging.FileHandler(path))