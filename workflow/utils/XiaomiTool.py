import json
import requests
import hashlib
from Crypto.PublicKey import RSA
import Crypto.Signature.PKCS1_v1_5 as sign_OKCS1_v1_5
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
from Crypto import Hash
from urllib import parse
import os.path

gXiaomiServiceUrl = 'http://api.developer.xiaomi.com/devupload'
gQueryUri = '/dev/query'
gCateUri = '/dev/category'
gPushApiUri = '/dev/push'
gUserName = 'zhangjianwei@iot.chinamobile.com'

class XiaomiTool:
    def __init__(self,certPath,privatePwd):
        if privatePwd is None:
            raise Exception('pwd is null')
        if certPath is None:
            raise Exception('cert path is null')
        if os.path.exists(certPath) != True:
            raise Exception('cert path is not exist')
        self.__certPath = certPath
        self.__privatePwd = privatePwd
        publicPem = open(self.__certPath).read()
        publicKey = RSA.importKey(publicPem)
        self.__cipherObject = PKCS1_v1_5.new(publicKey)

    def encryptStr(self,targetStrToEncrypt):
        '采用公钥进行加密'
        if self.__cipherObject is None:
            raise Exception('ciper object is not exist')
        tResult = []
        targetStrEncode = targetStrToEncrypt.encode(encoding='UTF-8')
        targetStrLength = len(targetStrEncode)
        sliceStepCount = targetStrLength // 100
        sliceStepMovalue = targetStrLength % 100
        if sliceStepCount == 0:
            tEncryStr = self.__cipherObject.encrypt(targetStrEncode)
            tResult.append(tEncryStr.hex())
        else:
            for i in range(0,sliceStepCount):
                tEncryStr = self.__cipherObject.encrypt(targetStrEncode[100*i : (i+1)*100])
                tResult.append(tEncryStr)
            if sliceStepMovalue != 0:
                tEncryStr = self.__cipherObject.encrypt(targetStrEncode[sliceStepCount*100 : sliceStepCount*100 + sliceStepMovalue])
                tResult.append(tEncryStr)
        covertRs = []
        for subBytes in tResult:
            for oneByte in subBytes:
                covertRs.append(oneByte)
        hexStr = ''.join(['%02x' % b for b in covertRs])
        return hexStr

    def getFileMd5Value(self,targetFilePath):
        '计算文件的MD5值'
        if targetFilePath is None:
            raise Exception('file path is None')
        if os.path.exists(targetFilePath) != True:
            raise Exception('file is not exist')
        with open(targetFilePath,'rb') as f:
            md5Obj = hashlib.md5()
            md5Obj.update(f.read())
            tHashValue = md5Obj.hexdigest()
            return str(tHashValue).lower()


    def queryAppInfo(self,appInfoJson):
        '从平台查询包信息'
        jsonStr = json.dumps(appInfoJson)
        paramMd5HexValue = hashlib.md5(jsonStr.encode(encoding='UTF-8')).hexdigest()
        formParams = []
        formParams.append({'RequestData':jsonStr})
        sig = {}
        sigs = []
        tSig = {}
        tSig['name'] = 'RequestData'
        tSig['hash'] = paramMd5HexValue
        sigs.append(tSig)
        sig['sig'] = sigs
        sig['password'] = self.__privatePwd
        strToEncry = json.dumps(sig)
        strAfterEncry = self.encryptStr(strToEncry)
        formParams.append({'SIG':strAfterEncry})
        nameOneUrlCode = parse.quote('RequestData')
        valueOneUrlCode = parse.quote(jsonStr)
        keyAndValueOne = nameOneUrlCode + '=' + valueOneUrlCode
        nameTwoUrlCode = parse.quote('SIG')
        valueTwoUrlCode = parse.quote(strAfterEncry)
        keyAndValueTwo = nameTwoUrlCode + '=' + valueTwoUrlCode
        formStrToPost = keyAndValueOne + '&' + keyAndValueTwo
        formStrToPostByte = formStrToPost.encode('UTF-8')
        tQueryUrl = gXiaomiServiceUrl + gQueryUri
        responseContent = requests.post(url=tQueryUrl,data=formStrToPostByte,headers={'Content-Type':'application/x-www-form-urlencoded'})
        resultStr = responseContent.text
        return resultStr

    def queryCategary(self):
        '查询分类'
        tQueryCateUrl = gXiaomiServiceUrl + gCateUri
        responseContent = requests.post(url=tQueryCateUrl)
        resultStr = responseContent.text
        return resultStr

    def pushApkInfo(self,appBaseInfo,apkFilePath,iconFilePath,screenShots):
        '推送信息包'
        baseInfoJsonStr = json.dumps(appBaseInfo)
        baseInfoMd5HexStr = hashlib.md5(baseInfoJsonStr.encode(encoding='UTF-8')).hexdigest()
        paramMdsArray = []
        sigItem = {}
        sigItem['name'] = 'RequestData'
        sigItem['hash'] = baseInfoMd5HexStr
        paramMdsArray.append(sigItem)
        fileEntitys = {}
        if apkFilePath is not None:
            apkInfo = {}
            apkInfo['name'] = 'apk'
            apkFileMd5Value = self.getFileMd5Value(apkFilePath)
            apkInfo['hash'] = apkFileMd5Value
            paramMdsArray.append(apkInfo)
            fileEntitys['apk'] = open(apkFilePath,'rb')
        if iconFilePath is not None:
            iconInfo = {}
            iconInfo['name'] = 'icon'
            iconFileMd5Value = self.getFileMd5Value(iconFilePath)
            iconInfo['hash'] = iconFileMd5Value
            paramMdsArray.append(iconInfo)
            fileEntitys['icon'] = open(iconFilePath,'rb')
        if screenShots is not None and len(screenShots) > 0:
            if len(screenShots) > 5:
                raise Exception('screenshots max could not exceed 5')
            for i in range(len(screenShots)):
                screenPath = screenShots[i]
                screenName = 'screenshot_' + str(i + 1)
                screenInfo = {}
                screenInfo['name'] = screenName
                screenInfo['hash'] = self.getFileMd5Value(screenPath)
                paramMdsArray.append(screenInfo)
                fileEntitys[screenName] = open(screenPath,'rb')
        sigJson = {}
        sigJson['sig'] = paramMdsArray
        sigJson['password'] = self.__privatePwd
        dataJson = {}
        dataJson['RequestData'] = baseInfoJsonStr
        dataJson['SIG'] = self.encryptStr(json.dumps(sigJson))
        '接口调用'
        tPushUrl = gXiaomiServiceUrl + gPushApiUri
        responseContent = requests.post(url=tPushUrl,data=dataJson,files=fileEntitys)
        return responseContent.text
