import os
from workflow.task import Task
from workflow.utils import env as ENV

class Shell(Task):
    def __init__(self, *args, **kwargs):
        self.cmd = kwargs.get('cmd')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=Shell')

    def exec(self):
        self.info()
        os.chdir(os.path.join(self.workspace, ENV.GET('name')))
        os.system(self.cmd)