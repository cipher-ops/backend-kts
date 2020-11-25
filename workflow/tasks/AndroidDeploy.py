import os
import wget
from workflow.task import Task
from workflow.utils.ansible import Ansible
from workflow.utils import env as ENV
from kratos.apps.artifact.models import Artifact
from kratos.apps.service.serializers import ServiceSerializer
from kratos.apps.service.models import Service

class AndroidDeploy(Task):
    def __init__(self, *args, **kwargs):
        self.servers = kwargs.get('servers')
        self.artifact_id = kwargs.get('artifact_id')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=AndroidDeploy')

    def exec(self):
        self.info()

        artifact = Artifact.objects.get(pk=self.artifact_id)
        # 切换到工作目录
        os.chdir(self.workspace)
        # 下载制品到本地工作区
        self.logger.info('下载制品至本地工作区...')
        out_fname = ENV.GET('name') + '-' + artifact.version + '.apk'
        wget.download(artifact.download_url, out=out_fname)
        # Ansible初始化
        self.logger.info('上传apk至服务器...')
        ansible = Ansible(servers=self.servers, connection='smart', become=True, become_method='sudo')
        ansible.run(
            module='file',
            args='path=%s state=directory' % (
                os.path.join(
                    self.remote_appbase,
                    ENV.GET('name'),
                    artifact.version
                ),
            )
        )
        ansible.run(
            module='copy',
            args='src=%s dest=%s' % (
                out_fname,
                os.path.join(
                    self.remote_appbase,
                    ENV.GET('name'),
                    artifact.version
                )
            )
        )
        ansible.get_result()
        os.unlink(out_fname)
        self.logger.info('Android部署完成!')

        # APK部署完成，服务信息入库
        self.logger.info('服务信息入库...')
        for server in self.servers:
            Service.objects.update_or_create(
                server_id=server,
                app_id=ENV.GET('app_id'),
                app_version=artifact.version
            )
        self.logger.info('服务信息入库完成! 任务执行完毕!')
