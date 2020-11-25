import os
import tempfile
from workflow.task import Task
from workflow.utils import env as ENV
from kratos.apps.configuration import models
from kratos.apps.configuration import serializers
from kratos.apps.service.models import Service
from workflow.utils.ansible import Ansible

class ConfigDeploy(Task):
    def __init__(self, *args, **kwargs):
        self.servers = kwargs.get('servers')
        self.configs = kwargs.get('configs')
        self.app_version = ENV.GET('app_version', kwargs.get('app_version'))
        self.config_version = ENV.GET('config_version', kwargs.get('config_version'))
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=ConfigDeploy')

    def exec(self):
        self.info()
        # 配置库中拉取配置
        configs = serializers.ConfigurationSerializer(
            models.Configuration.objects.filter(pk__in=self.configs, version=self.config_version, app=ENV.GET('app_id')),
            many=True
        ).data

        # 配置推送
        self.logger.info('开始配置部署...')
        ansible = Ansible(servers=self.servers, connection='smart', become=True, become_method='sudo')
        for config in configs:
            # 目录创建
            ansible.run(
                module='file',
                args='path=%s state=directory' % (
                    os.path.join(
                        self.remote_appbase, 
                        ENV.GET('name'), 
                        self.app_version, 
                        config['path'] if config['path'] else ''
                    ),
                )
            )

            # 创建临时文件用于缓存配置
            f = tempfile.NamedTemporaryFile(mode='w+', delete=False)
            f.write(config['content'])
            f.close()
            # 执行配置copy
            ansible.run(
                module='copy',
                args='src=%s dest=%s' % (
                    f.name,
                    os.path.join(
                        self.remote_appbase, 
                        ENV.GET('name'), 
                        self.app_version, 
                        config['path'] if config['path'] else '',
                        config['name']
                    )
                )
            )
            # copy完毕删除临时配置文件
            os.unlink(f.name)
        ansible.get_result()
        self.logger.info('配置部署完成!')

        # 更新服务信息
        self.logger.info('服务信息更新...')
        for server in self.servers:
            Service.objects.update_or_create(
                server_id=server,
                app_id=ENV.GET('app_id'),
                app_version=self.app_version,
                defaults={'config_version': self.config_version}
            )
        self.logger.info('服务信息更新完成! 任务执行完毕!')
