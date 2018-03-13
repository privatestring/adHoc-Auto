#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : joker

from optparse import OptionParser
import subprocess
import os,sys,fileinput,getpass,shutil
import json
import urllib,urllib2
import keys


#钉钉消息
DINT_PACKAGE_START = {"msgtype": "text",  "text": {"content": "iOS打包：\n %s开始打包了，请等待几分钟\n查看打包详情：%s \n @所有人 "},"isAtAll":True}
DINT_PACKAGE_END = {"msgtype": "text",  "text": {"content": "iOS打包：\n %s已发布最新测试版\n前往下载：%s \n @所有人 "},"isAtAll":True}
#上传pgyer失败给下载链接
JENKINS_SAVE_DIR = '/Users/ring/Public/webSites/monkey_log'


#获取项目名称
def getProjectName():
    path = provideRootDir()
    for file in os.listdir(path):
        if("xcworkspace" in file):
            return file.split('.')[0]


#启动打印函数
def printStart(version):
    project_name = getProjectName()
    print "*****************************************************************"
    print "*****************************************************************"
    print "                       开始打包                             "
    print "  项目名称：%s" %(project_name)
    print "  版 本 号：%s" %(version)
    print "  打包人员：%s" %(getCurrUserName())
    print "  是否上传蒲公英：%s" %(keys.OPEN_PYUPLOAD)
    print "  输出路径：%s/%s/%s_%s.ipa" %(provideOutPut(),version,project_name ,version)
    print "*****************************************************************"
    print "*****************************************************************"
    if (isJenkinsPackage()):
        for token in keys.DING_LIST:
            sendToDing(token,False)

#结束打印函数
def printEnd(version):
    project_name = getProjectName()
    print "*****************************************************************"
    print "*****************************************************************"
    print "                       结束打包                             "
    print "  项目名称：%s" %(project_name)
    print "  版 本 号：%s" %(version)
    print "  打包人员：%s" %(getCurrUserName())
    print "  是否上传蒲公英：%s" %(keys.OPEN_PYUPLOAD)
    print "  输出路径：%s/%s/%s_%s.ipa" %(provideOutPut(),version,project_name,version)
    print "*****************************************************************"
    print "*****************************************************************"

def isJenkinsPackage():
    return keys.JENKINS_NAME in getCurrUserName()
# 修改版本号
def changeVersion(preVersion,currVersion):
    f = open(provideInfoPlist(),mode='r+')
    s = f.read()
    f.seek(0,0)
    f.write(s.replace(preVersion,currVersion))
    f.close()
	# changeVer = '/usr/libexec/PlistBuddy -c \"Set :CFBundleShortVersionString %s\" %s' %(version,provideInfoPlist())
	# process = subprocess.Popen(changeVer, shell = True)
	# process.wait()

#获取当前电脑用户名
def getCurrUserName():
    return getpass.getuser()

#获取rootDir
def provideRootDir():
    return os.path.abspath(keys.ROOT_LOCATION)

#获取输出目录
def provideOutPut():
    createDir(os.path.abspath(keys.OUTPUT))
    return os.path.abspath(keys.OUTPUT)

#获取info.plist
def provideInfoPlist():
    path = '%s/%s/SuggestFile/info.plist' %(provideRootDir(),getProjectName())
    if(os.path.exists(path)==False):
        path = '%s/%s/info.plist' %(provideRootDir(),getProjectName())
    return path

#清除 build 目录
def cleanBuildDir(buildDir):
	cleanCmd = "rm -r %s" %(buildDir)
	process = subprocess.Popen(cleanCmd, shell = True)
	process.wait()

def copyFile(isDir,originalPath,filePath):
    print "是否存在 = %s" %(os.path.exists(filePath))
    print "目标文件 = %s" %originalPath
    print "复制到  = %s" %filePath
    if os.path.exists(filePath):
        if isDir == True:
            shutil.rmtree(filePath)
        else:
            os.remove(filePath)
    createDir(os.path.dirname(filePath))
    if isDir == True:
        shutil.copytree(originalPath,filePath)
    else :
        shutil.copyfile(originalPath,filePath)

#获取文件夹下最新文件
def getLastFileFromDir(file_dir):
    if not os.path.exists(file_dir):
        return ''
    file_dict = {}
    lists = os.listdir(file_dir) #先获取文件夹内的所有文件
    for f in lists:
        if 'xcarchive' in f:
            ctime = os.stat(os.path.join(file_dir, f)).st_ctime
            file_dict[ctime] = f # 添加创建时间和文件名到字典
    if(len(file_dict)>0):
        max_ctime = max(file_dict.keys()) # 取值最大的时间
        return file_dict[max_ctime] #返回最新文件名
    else:
        return ""
#创建路径
def createDir(dirPath):
    if not os.path.exists(dirPath):
        os.makedirs(dirPath)

#创建文件
def createFile(filePath,inputStr):
    createDir(os.path.dirname(filePath))
    output = open(filePath,'w')
    output.write(inputStr)
    output.close()

#获取当前版本号，不加beta
def getLocalVersion():
    return getLocalCompileVersion().split('_beta')[0]
#获取当前完整版本号
def getLocalCompileVersion():
    num_line = 0
    path = provideInfoPlist()
    for line in fileinput.input(path):
        num_line = num_line + 1
        if ('CFBundleShortVersionString' in line)  :
            break
    fileinput.close()
    f = open(path)
    version = f.readlines()[num_line].replace('string','').replace('<','').replace('>','').replace('/','').replace('\n','').replace(' ','').strip()
    f.close()
    return version


#获取最新beta版本
def getLastBetaVersion(version):
    print "\n\n***************获取pgyer上最新版本中*********************\n"
    if('beta' in version) :
        return version
    else :
        betaNum = 0
        for data in getPgyerVersionList():
            v = data["buildVersion"]
            if(version in v) :
                betaStr = v.split('beta')
                print v
                if(len(betaStr)>1 and int(betaStr[1])>betaNum):
                    betaNum = int(betaStr[1])
        return version+"_beta"+str(betaNum+1)

#获取pgyer版本列表
def getPgyerVersionList():
    project_name = getProjectName();
    app_key = keys.PGYER_APP_KEY[project_name]
    url = 'https://www.pgyer.com/apiv2/app/builds'
    values = {'_api_key':keys.PGYER_API_KEY,'appKey':app_key,'page':0}
    data = urllib.urlencode(values) # 编码工作
    req = urllib2.Request(url, data)  # 发送请求同时传data表单
    response = urllib2.urlopen(req)  #接受反馈的信息
    listData = json.loads(response.read())["data"]["list"]  #读取反馈的内容
    return listData

#上传pgyer
def uploadPgy(ipaPath):
    print "\n***************开始上传到蒲公英*********************\n"
    # uploadCmd = 'curl -F \"file=@%s\" -F \"_api_key=%s\" https://www.pgyer.com/apiv2/app/upload' %(ipaPath,keys.PGYER_API_KEY)
    # print uploadCmd
    # process = subprocess.Popen(uploadCmd,shell = True)
    # process.wait()
    status = os.system("sh ./shell/reportPgyer.sh %s" %(ipaPath))
    print status
    if(status == 0):#上传成功
        print "\n\n***************上传结束 Code=0 为上传成功*********************\n"
        for token in keys.DING_LIST:
            sendToDing(token,True)
    elif(isJenkinsPackage()):
        print "\n\n***************上传pgyer失败 请前往http://fbi.com:8888/monkey_log 下的ios下载上传失败文件%s，手动上传pgyer *********************\n" %(os.path.basename(ipaPath))
        print os.path.basename(ipaPath)
        dirPath = "%s/ios/%s" %(JENKINS_SAVE_DIR,getProjectName())
        createDir(dirPath)
        copyFile(False,ipaPath,"%s/%s" %(dirPath,os.path.basename(ipaPath)))
    else :
        print "\n\n***************上传pgyer失败 上传失败文件%s，手动上传pgyer *********************\n" %(ipaPath)

#上传符号表文件到bugly
def uploadBugly(appSymboPath,projectName,version):
    buglyInfo = keys.BUGLY_INFO[projectName]
    status = os.system("sh ./shell/reportBugly.sh %s %s %s %s %s" %(appSymboPath,buglyInfo['id'],buglyInfo['key'],buglyInfo['package'],version))
    if(status == 0):#上传成功
        print "\n\n***************上传Bugly结束 Code=0 为上传Bugly成功*********************\n"
    elif(isJenkinsPackage()):
        print "\n\n***************上传Bugly失败 请前往http://fbi.com:8888/monkey_log 下的ios下载上传失败文件%s，手动上传bugly *********************\n" %(os.path.basename(appSymboPath))
        print os.path.basename(appSymboPath)
        dirPath = "%s/ios/%s" %(JENKINS_SAVE_DIR,getProjectName())
        copyFile(True,appSymboPath,"%s/%s" %(dirPath,os.path.basename(appSymboPath)))
    else :
        print "\n\n***************上传Bugly失败 上传失败文件%s，手动上传bugly *********************\n" %(appSymboPath)

#创建自动上传脚本
def createUploadShell(projectName,version):
    buglyInfo = keys.BUGLY_INFO[projectName]
    line1 = '#!/bin/bash'
    line2 = 'currPath=$(cd \"$(dirname \"%s\")\";pwd)' %(os.path.abspath('./shell/reportBugly.sh'))
    line3 = 'echo 正在上传bugly'
    base = 'java -jar $currPath/buglySymboliOS.jar -i $1 -u -id %s -key %s -package %s -version %s' %(buglyInfo['id'],buglyInfo['key'],buglyInfo['package'],version)
    line4 = 'echo %s' %base
    sh =  "%s/%s/bugly.sh"%(provideOutPut(),version)
    createFile(sh,'%s\n%s\n%s\n%s\n%s' %(line1,line2,line3,line4,base))


def sendToDing(token,isOver):
    projectInfo = keys.PROJECT_INFO_LIST[getProjectName()]
    if isOver:
        jsonData = DINT_PACKAGE_END
        jsonData['text']['content'] = jsonData['text']['content'] %(projectInfo['name'],projectInfo['url'])
    else :
        jsonData = DINT_PACKAGE_START
        jsonData['text']['content'] = jsonData['text']['content'] %(projectInfo['name'],projectInfo['fbi'])
    jsonData = json.dumps(jsonData, ensure_ascii=False, encoding='UTF-8')
    url = "https://oapi.dingtalk.com/robot/send?access_token="+token
    dingCmd = 'curl %s -H \'Content-Type:application/json\' -d \'%s\'' %(url,jsonData)
    process = subprocess.Popen(dingCmd,shell = True)
    process.wait()
