#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : joker

# JokerDemo是joker用来测试的项目，不要管它

# 需要改动的地方 (根据自己的项目信息改动改动)
ROOT_LOCATION = "../.."
#打包导出ipa文件路径
OUTPUT = ROOT_LOCATION+"/Packge"

#服务器电脑名
JENKINS_NAME = "jenkins"
#如果一定要用xcode打包，请在下面数组加上你的电脑名,不建议使用xcode打包
IGNORE_LIST = []#,'joker'

#打包完成发送给钉钉
DING_LIST=['钉钉机器人的token']

#蒲公英上传
OPEN_PYUPLOAD = False  	#是否开启蒲公英上传功能  True  False
PGYER_API_KEY = "xxxx"
PGYER_APP_KEY = {"Demo":"xxxxx"}
# 是否上传符号表
OPEN_BUGLY_UPLOAD = False
#bugly相关信息
BUGLY_INFO = {"Demo":{"id":"0000","key":"xxxx","package":"com.demo.xxx"}}

#项目相关pgyer信息
PROJECT_INFO_LIST = {"Demo":{"name":"项目名","url":"https://www.pgyer.com/下载地址","fbi":"jenkins地址，可以没有"}}
