#!/bin/bash
workSpace=$(cd "$(dirname "$0")";pwd)
echo $workSpace
cd $workSpace
pwd
sh ./package.sh
