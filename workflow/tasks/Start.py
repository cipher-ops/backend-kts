import os
from workflow.task import Task
from workflow.utils.ansible import Ansible

class Start(Task):
    def __init__(self, *args, **kwargs):
        self.cmd = kwargs.get('cmd')
        self.servers = kwargs.get('servers')

    def info(self):
        self.logger.info('TaskName=Start')

    def exec(self):
        self.info()

        ansible = Ansible(inventory=self.servers['inventory'], connection='smart', become=True, become_method='sudo')
        ansible.run(hosts=','.join(self.servers['hosts']), module='shell', args=self.cmd)
        ansible.get_result()        