#!/bin/bash
workSpace=$(cd "$(dirname "$0")";pwd)
echo $workSpace
cd $workSpace
pwd
python ./prepare.py
python ./autoPackage.py
