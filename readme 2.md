# 自动打包集成
# Version-1
## 加新项目集成
1. 在keys.py中的PGYER_APP_KEY 加入项目名称及pgyer上的appkey
2. PROJECT_INFO_LIST 加入项目名称及中文名称，pgyer下载地址，jenkins打包地址

## 开始使用
1. 进入 ./externals/bistg/adHoc-Auto/下
2. 本地打包：以下方式都可以
  * 双击package.command文件出现打包命令行界面（注意，如果报错，可能是没有权限行动，请在命令行中执行 （chmod a+x 打包详细文件地址）后再次双击就行）
  * 在命令行中执行 sh package.sh  
  * 在命令行中执行 python autoPackage.py (后面可传入参数版本号，版本号不要加beta，beta版本会自动升级)

## 打包成功后异常
打包成功后，但可能网络出故障，上传pgyer失败时，请前往http://fbi.com:8888/monkey_log/ios 下获取ipa原文件手动上传pgyer

# Version-2
## bugly符号表优化
新加bugly符号表分离上传，至少节省（6-8）分钟（网络比较好的时候，如果不好可以节省更多），不影响非beta版
## 非得用xcode打包，可用以下配置
  ```（不建议使用，时间太长) ```
  1. 在key.py下的IGNORE_LIST 数组中加上你的电脑名
  2. 手动上传 自己在根目录下的 Package/版本号/ 下打开命令行工具，执行命令 sh bugly.sh xxx  (xxx 是当前文件夹下的xx.app.dSYM)
