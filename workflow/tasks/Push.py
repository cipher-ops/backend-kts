import os
import wget
from workflow.task import Task
from workflow.utils.ansible import Ansible
from workflow.utils import env as ENV

'''
从制品库拉，然后push到部署服务的机器
'''
class Push(Task):
    def __init__(self, *args, **kwargs):
        self.src = kwargs.get('src')
        self.dst = kwargs.get('dst')
        self.servers = kwargs.get('servers')
        self.unarchive = kwargs.get('unarchive')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=Push')


    def exec(self):
        self.info()

        working_dir = os.path.join(self.workspace, ENV.GET('name'))
        os.chdir(working_dir)
        appsurl = AppArtifacts.objects.filter(app_id=ENV.GET('app_id'), version=ENV.GET('version', '1.0.1'))

        self.logger.info(appsurl[0].download_url)

        out_fname = wget.filename_from_url(appsurl[0].download_url)
        self.logger.info('out_fname: '+out_fname)

        if os.path.exists(os.path.join(working_dir, out_fname)):
            self.logger.info('file exists, removing it...')
            os.remove(out_fname)
        
        #src_path 为本地缓存目录，不同于数据库中的src
        wget.download(appsurl[0].download_url, out=out_fname)
        os.chdir(self.workspace)
        self.logger.info('entering... '+self.workspace)
        src_path = os.path.join(self.workspace, self.src, out_fname)
        dst_path = self.dst

        #推送到部署服务的主机，dst目录不存在则创建；远程文件存在，内容不同于源时，将替换远程文件；
        ansible = Ansible(inventory=self.servers['inventory'], connection='smart', become=True, become_method='sudo')
        if self.unarchive:
            self.logger.info('unarchive: '+str(self.unarchive))
            ansible.run(hosts=','.join(self.servers['hosts']), module='unarchive', args='src=%s dest=%s' % (src_path, dst_path))
        else:
            self.logger.info('unarchive: '+str(self.unarchive))
            ansible.run(hosts=','.join(self.servers['hosts']), module='copy', args='src=%s dest=%s' % (src_path, dst_path))
        self.logger.info('ansible result: '+str(ansible.get_result()))
        
        #完成后，清理下载的临时文件
        if os.path.exists(os.path.join(working_dir,out_fname)):
            self.logger.info('push ok, removing donwload tmp file...')
            os.remove(os.path.join(working_dir,out_fname))