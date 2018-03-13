#!/bin/bash
echo "正在上传的文件 $1"
echo "下在上传,请等一小会儿"
curl -F "file=@$1" -F "uKey=cdff98216554393da001ebfc75bde623" -F "_api_key=1bd4e19be1499a3faf7114659b7d3f7f" https://qiniu-storage.pgyer.com/apiv1/app/upload
