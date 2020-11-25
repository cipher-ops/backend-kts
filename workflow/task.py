from abc import ABCMeta, abstractmethod
from .utils.logger import Logger

class Task(object):
    __metaclass__ = ABCMeta

    workspace = '/data/kts/workspace'
    remote_appbase = '/data/kts/apps'

    # logger = Logger().logger

    @abstractmethod
    def exec(self):
        pass