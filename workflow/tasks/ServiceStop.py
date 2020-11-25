import os
from workflow.task import Task
from workflow.utils.ansible import Ansible
from workflow.utils import env as ENV
from kratos.apps.service.models import Service

class ServiceStop(Task):
    def __init__(self, *args, **kwargs):
        self.deploy_apth = kwargs.get('deploy_path')
        self.app_version = ENV.GET('app_version', kwargs.get('app_version'))
        self.cmd = kwargs.get('cmd')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=ServiceStop')

    def exec(self):
        self.info()

        # 获取服务信息
        services = Service.objects.filter(app_id=ENV.GET('app_id'), app_version=self.app_version)

        # Ansible初始化
        ansible = Ansible(servers=[service.server.id for service in services], connection='smart', become=True, become_method='sudo')

        # 执行停服命令
        self.logger.info('执行停止命令...')
        ansible.run(
            module='shell',
            args=self.cmd
        )

        # 删除应用软连接
        self.logger.info('删除应用软连接...')
        ansible.run(
            module='file',
            args='path=%s state=absent' % self.deploy_apth
        )

        # 获取执行结果
        ansible.get_result()

        # 更新服务信息
        services.update(status=2)

        self.logger.info('服务关闭完成! 任务执行完毕!')
