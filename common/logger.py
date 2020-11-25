#!/usr/bin/env python
# -*- coding:utf-8 -*-
#from django.conf import settings
import logging

class Logger():
    @staticmethod
    def log(message, type='info'):
        '''
        说明:
            打印日志
        参数:
            message, 打印日志消息
            type, 日志类型,支持 info,debug,error,默认值为info
        返回值:
            无
        作者:liaoyugen
        时间:2017/11/27
        '''

        logger = logging.getLogger('django')

        if type.lower().strip() == 'info':
            logger.info(message)
        elif type.lower().strip() == "debug":
            logger.debug(message)
        elif type.lower().strip() == "error":
            logger.error(message)