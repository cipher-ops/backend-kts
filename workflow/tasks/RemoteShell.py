import os
from workflow.task import Task
from workflow.utils import env as ENV
from workflow.utils.ansible import Ansible

class RemoteShell(Task):
    def __init__(self, *args, **kwargs):
        self.cmd = kwargs.get('cmd')
        self.servers = kwargs.get('servers')
        self.inventory = kwargs.get('inventory')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=Remoteshell')
    
    #通过ansible接口 在远程主机执行shell命令
    def exec(self):
        self.info()
        ansible = Ansible(servers=self.servers, connection='smart', become=True, become_method='sudo')
        #调用ansible接口，在远程主机执行传入的cmd
        #ansible.run(hosts=','.join(self.servers['hosts']), module='command', args='cmd=%s' % (self.cmd))
        ansible.run(module='shell', args=self.cmd)
        ansible.get_result()