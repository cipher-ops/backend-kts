import os
from workflow.task import Task
from workflow.utils.git.repo import Repo
from workflow.utils import env as ENV

class Clone(Task):
    def __init__(self, *args, **kwargs):
        self.repo = kwargs.get('repo')
        self.type = kwargs.get('type')
        self.branch = kwargs.get('branch')
        self.commit = kwargs.get('commit')
        self.tag = kwargs.get('tag')
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=Clone')

    def exec(self):
        self.info()
        os.chdir(self.workspace)
        to_path = os.path.join(self.workspace, ENV.GET('name'))
        repo = Repo(to_path)
        repo.init(url=self.repo)

        if self.type == 'tag':
            repo.checkout_2_tag(self.tag)
        elif self.type == 'branch':
            if self.commit:
                repo.checkout_2_commit(self.branch, self.commit)
            else:
                repo.checkout_2_branch(self.branch)
                repo.pull()
