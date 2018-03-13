#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : joker

from optparse import OptionParser
import subprocess
import os,sys,time,shutil
import support,keys,autoPackage
import json

def releaseBugly(symbolPath,productName,version):
    print "this is release version ,need autom report Symbo to bugly "
    support.uploadBugly(appSymboPath=symbolPath,projectName=productName,version=version)

def testAdHoc(symbolPath,productName,version):
    if(support.getCurrUserName() in keys.IGNORE_LIST):
        print "这是忽略用xcode打包，程序自己上传，可能上传Bugly时间比较长，不建议使用"
        releaseBugly(symbolPath,productName,version)
    else:
        print "this is beta 版本 为了提高打包速度，bugly的symbo文件放在打包完成及上传pgyer完成后再上报，不影响上传bugly，只是调整顺序"

def exportXcarchive(productName,version):
    archiveDir = "/Users/%s/Library/Developer/Xcode/Archives"%support.getCurrUserName()
    ymd = time.strftime("%Y-%m-%d", time.localtime())
    lastFile = support.getLastFileFromDir("%s/%s"%(archiveDir,ymd))
    xcarchivePath = "%s/%s/%s"%(archiveDir,ymd,lastFile)
    print "%s  %s" %(compiletePath , os.path.exists(xcarchivePath))
    if os.path.exists(compiletePath):
        autoPackage.xcbuildExportArchive(version,compiletePath,projectName)


def main():
    if(len(sys.argv) > 2 ):#解析参数
        configBuildDir = sys.argv[1]
        productName = sys.argv[2]
        compileVersion = support.getLocalCompileVersion()
        for arg in sys.argv:
            print "参数 %s " %arg
        #拼接参数获取symbol文件
        symbolPath = "%s/%s.app.dSYM" %(configBuildDir,productName)
        if(not os.path.exists(symbolPath)):
            print "\n\n*******************************************\n"
            print "\n\n******当前目录文件不存在，app打包未成功，无法上传bugly\n%s******\n"%symbolPath
            print "\n\n*******************************************\n"
        else:#备份到output下
            print os.path.basename(symbolPath)
            dirPath = "%s/%s" %(support.provideOutPut(),compileVersion)
            resultPath = "%s/%s" %(dirPath,os.path.basename(symbolPath))
            support.copyFile(True,symbolPath,resultPath)
            support.createUploadShell(productName,compileVersion)
            if('beta' in compileVersion):
                testAdHoc(resultPath,productName,compileVersion)
            else :
                releaseBugly(resultPath,productName,compileVersion)
    else :
        print "\n\n***************传参失败*********************\n"
        print "\n\n*******************************************\n"
        print "\n\n**********请在项目中的build phases中执行*******\n"
        print "cd $SRCROOT/externals/bistg/adHoc-Auto"
        print "/usr/bin/python buglySymbol.py $CONFIGURATION_BUILD_DIR $PRODUCT_NAME"
        print "\n\n*******************************************\n"
        print "\n\n*******************************************\n"
        print "\n\n***************传参失败*********************\n"



if __name__ == '__main__':
	main()
