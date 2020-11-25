import os
from workflow.task import Task
from workflow.utils.ansible import Ansible
from workflow.utils import env as ENV
from kratos.apps.artifact.models import Artifact
from kratos.apps.service.serializers import ServiceSerializer
from kratos.apps.service.models import Service

class DockerDeploy(Task):
    def __init__(self, *args, **kwargs):
        self.servers = kwargs.get('servers')
        self.artifact_id = kwargs.get('artifact_id')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=DockerDeploy')

    def exec(self):
        self.info()

        artifact = Artifact.objects.get(pk=self.artifact_id)
        
        # 在目标服务器上下载Docker镜像
        self.logger.info('开始下载镜像...')
        ansible = Ansible(servers=self.servers, connection='smart', become=True, become_method='sudo')
        ansible.run(module='shell', args='docker pull %s' % artifact.download_url)
        ansible.get_result()
        self.logger.info('镜像下载完成!')

        # Docker部署完成，服务信息入库
        self.logger.info('服务信息入库...')
        for server in self.servers:
            Service.objects.update_or_create(
                server_id=server,
                app_id=ENV.GET('app_id'),
                app_version=artifact.version
            )
        self.logger.info('服务信息入库完成! 任务执行完毕!')
