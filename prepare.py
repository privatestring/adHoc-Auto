#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : joker

from optparse import OptionParser
import subprocess
import os,sys
import support,keys
import json

def prepare(version):
    support.changeVersion(support.getLocalCompileVersion(),version)
    support.printStart(version)

def main():
    version = support.getLocalVersion()
    if len(sys.argv)>1 :
        version = sys.argv[1]
    version = support.getLastBetaVersion(version)
    prepare(version)
    print "----"+version+"----"




if __name__ == '__main__':
	main()
