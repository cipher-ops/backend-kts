import os
import json
import requests
from workflow.task import Task
from workflow.utils import env as ENV
from workflow.utils.XiaomiTool import XiaomiTool
from collections import defaultdict

class ApkToXiaomi(Task):
    def __init__(self, *args, **kwargs):
        self.ApkFilePath = kwargs.get('ApkFilePath')
        self.IconFilePath = kwargs.get('IconFilePath')
        self.ScreenShotFilePath = kwargs.get('ScreenShotFilePath').split(',')
        self.PublicKey = kwargs.get('PublicKey')
        ##注意私钥有过期时限大概是30天以内
        self.PrivateKey = kwargs.get('PrivateKey')
        self.desc = kwargs.get('desc')
        self.appName = kwargs.get('appName')
        self.category = kwargs.get('category')
        self.keyWords = kwargs.get('keyWords')
        self.packageName = kwargs.get('packageName')
        self.userName = kwargs.get('userName')
        self.synchroType = kwargs.get('synchroType')

        self.RequestData = {}
        self.appInfo = self.RequestData.setdefault("appInfo",{})
        self.appInfo.setdefault("desc",self.desc)
        self.appInfo.setdefault("appName",self.appName)
        self.appInfo.setdefault("category",self.category)
        self.appInfo.setdefault("keyWords",self.keyWords)
        self.appInfo.setdefault("packageName",self.packageName)
        self.RequestData.setdefault("userName",self.userName)
        self.RequestData.setdefault("synchroType",self.synchroType)
        self.logger = ENV.GET('logger')

    def info(self):
        self.logger.info('TaskName=ApkToXiaomi')

    #PUSH APK文件到小米应用商店
    def exec(self):
        self.info()

        # 切换到工作目录
        os.chdir(self.workspace)
        # APK推送小米应用商店
        self.logger.info('APK推送小米应用商店...')

        xiaomiobj = XiaomiTool(self.PublicKey,self.PrivateKey)
        rsp = xiaomiobj.pushApkInfo(self.RequestData,self.ApkFilePath,self.IconFilePath,self.ScreenShotFilePath)

        if json.loads(rsp)["result"] == 0:
            self.logger.info('APK推送小米完成!')
        else:
            self.logger.info(json.loads(rsp)["message"])
