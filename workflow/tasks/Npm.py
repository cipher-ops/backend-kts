import os
import docker
from datetime import datetime
from workflow.task import Task
from workflow.utils import env as ENV

class Npm(Task):
    def __init__(self, *args, **kwargs):
        self.image = kwargs.get('image')
        self.cmd = kwargs.get('cmd')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=Npm')

    def exec(self):
        self.info()
        client = docker.from_env()
        working_dir = os.path.join(self.workspace, ENV.GET('name'))
        volumes = {}
        volumes[working_dir] = {'bind': working_dir, 'mode': 'rw'}
        self.logger.info('{} - Starting\n'.format(datetime.now()))
        container = client.containers.run(
            self.image, ['/bin/sh', '-c', self.cmd],
            volumes=volumes,
            working_dir=working_dir, 
            detach=True,
            remove=True
        )
        for line in container.logs(stream=True):
            self.logger.info(line.decode().strip())
        self.logger.info('\n{} - Completed\n'.format(datetime.now()))
