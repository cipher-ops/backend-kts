import os
import json
import requests
from datetime import datetime
from workflow.task import Task
from workflow.utils import env as ENV
from kratos.apps.artifact import models

class Artifact(Task):
    def __init__(self, *args, **kwargs):
        self.repo = kwargs.get('repo')
        self.version = ENV.GET('version', kwargs.get('version'))
        self.source = kwargs.get('source')
        self.token = kwargs.get('token')
        self.type = kwargs.get('type', 1)
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=Artifact')

    def exec(self):
        self.info()
        headers = {
            'Token': self.token
        }
        file = {
            'file': open(os.path.join(self.workspace, ENV.GET('name'), self.source), 'rb')
        }
        self.logger.info('{} - Starting\n'.format(datetime.now()))
        r = requests.post(url=self.repo, data={'version': self.version}, files=file, headers=headers)
        self.logger.info(r.text)
        if r.status_code == 200:
            meta_data = json.loads(r.text).get('data')
            models.Artifact.objects.update_or_create(
                app_id=ENV.GET('app_id'),
                artifact_type=self.type,
                version=meta_data.get('version'),
                defaults={'download_url': meta_data.get('downloadAddress'), 'size': meta_data.get('size')}
            )
        else:
            self.logger.error('Artifact Failed. ')
        self.logger.info('\n{} - Completed\n'.format(datetime.now()))