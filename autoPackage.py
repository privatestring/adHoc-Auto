#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : joker

from optparse import OptionParser
import subprocess
import os,sys
import support,keys
import json


#打包
def xcbuildArchive(version):
	project_name = support.getProjectName()
	xcarchivePath = './build/%s.xcarchive' %project_name
	print "当前正在打包的版本   %s" %version
	# 以下方法放到prepare中了
	# support.changeVersion(version)
	# support.printStart(version)
	#配置打包命令
	buildCmd = 'xcodebuild archive -workspace %s/%s.xcworkspace -scheme %s -sdk iphoneos -configuration Release  ONLY_ACTIVE_ARCH=NO -archivePath %s' %(support.provideRootDir(),project_name, project_name , xcarchivePath )

	#开始执行打包命令
	process = subprocess.Popen(buildCmd, shell = True)
	process.wait()

	if os.path.exists(xcarchivePath):
		xcbuildExportArchive(version,xcarchivePath,project_name)


#导出ipa包
def xcbuildExportArchive(version,xcarchivePath,projectName):
	outputDir = support.provideOutPut()
	#创建目录
	support.createDir(outputDir)

	#执行签名验证导出命令
	# signCmd = 'xcodebuild -exportArchive -archivePath ./build/JokerDemo.xcarchive -exportPath ../Packge/1.3.2 -exportOptionsPlist ../ext/AdHoc.plist'
	signCmd = 'xcodebuild -exportArchive -archivePath %s -exportPath %s/%s -exportOptionsPlist ./AdHoc.plist' %(xcarchivePath,outputDir,version)
	process = subprocess.Popen(signCmd, shell = True)
	process.wait()

	print signCmd

	support.printEnd(version)

	ipaPath = "%s/%s/%s.ipa" %(outputDir,version,projectName)
	print ipaPath
	newIpaPath = "%s/%s/%s_%s.ipa" %(outputDir,version,projectName ,version)
	os.rename(ipaPath,newIpaPath)

	print "ipa输出路径------>   【  "+newIpaPath+"   】"

	#蒲公英上传
	if keys.OPEN_PYUPLOAD == True:
		support.uploadPgy(newIpaPath)

	#上传bugly符号表
	if keys.OPEN_BUGLY_UPLOAD == True:
		symbolPath = "%s/%s/%s.app.dSYM" %(outputDir,version,projectName)
		print "上传bugly文件 ： %s"%(symbolPath)
		support.uploadBugly(symbolPath,projectName,version)

	#如果已经导包完成则，清理build目录
	if os.path.exists(newIpaPath):
		support.cleanBuildDir("./build")


def main():
	version = support.getLocalCompileVersion()
	xcbuildArchive(version)

	# 以下方法放到prepare中了
	# xcbuildArchive(support.getLastBetaVersion(version))
	# if len(sys.argv)>1 :
	# 	version = sys.argv[1]
	# version = support.getLastBetaVersion(version)
	# print "----"+support.getLastBetaVersion(version)+"----"




if __name__ == '__main__':
	main()
