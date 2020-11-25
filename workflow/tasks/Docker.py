import os
import docker
from datetime import datetime
from workflow.task import Task
from workflow.utils import env as ENV
from kratos.apps.artifact.models import Artifact

class Docker(Task):
    def __init__(self, *args, **kwargs):
        self.dockerfile = kwargs.get('dockerfile')
        self.dockerhub = kwargs.get('dockerhub')
        self.dockerRepo = kwargs.get('dockerRepo')
        self.imageName = kwargs.get('imageName')
        self.imageTag = ENV.GET('version', kwargs.get('imageTag'))
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=Docker')

    def exec(self):
        self.info()
        client = docker.from_env()
        working_dir = os.path.join(self.workspace, ENV.GET('name'))
        os.chdir(working_dir)
        self.logger.info('开始Docker构建...')
        # docker镜像构建
        _, logs = client.images.build(
            path=os.path.join(working_dir, self.dockerfile),
            tag='{}/{}/{}:{}'.format(self.dockerhub, self.dockerRepo, self.imageName, self.imageTag),
            rm=True,
            quiet=False
        )
        # 打印docker构建日志
        for log in logs:
            self.logger.info(log.get('stream')) if log.get('stream') else None
        
        # 上传docker镜像
        for line in client.images.push(
            repository='{}/{}/{}'.format(self.dockerhub, self.dockerRepo, self.imageName), 
            tag=self.imageTag,
            stream=True,
            decode=True
        ):
            self.logger.info(line.get('status')) if line.get('status') else None
        
        # 制品入库
        Artifact.objects.update_or_create(
            app_id=ENV.GET('app_id'),
            artifact_type=2,
            version=self.imageTag,
            download_url='{}/{}/{}:{}'.format(self.dockerhub, self.dockerRepo, self.imageName, self.imageTag),
            defaults={'size': 0}
        )
        self.logger.info('\n{} - Completed\n'.format(datetime.now()))