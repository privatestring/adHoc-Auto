#!/bin/bash
currPath=$(cd "$(dirname "$0")";pwd)
echo 正在上传bugly
echo java -jar $currPath/buglySymboliOS.jar -i $1 -u -id $2 -key $3 -package $4 -version $5
java -jar $currPath/buglySymboliOS.jar -i $1 -u -id $2 -key $3 -package $4 -version $5
