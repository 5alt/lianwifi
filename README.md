#wifi万能钥匙网页版

##简介

脚本会开启http服务，模拟mac版wifi万能钥匙进行wifi密码的查询

查询页面：

`http://<hosthost>:<port>/index`

提示查询过于频繁，更新认证信息：

`http://<hosthost>:<port>/refresh`

如有侵权，请联系作者删除代码

基于WiFi万能钥匙Mac客户端V1.1.0版开发（ 更新日期：2014-07-22）

##依赖的python库

```
sudo pip install flask
sudo pip install requests
sudo pip install pycrypto
sudo pip install celery
sudo pip install redis
sudo pip install celery-with-redis
```

##依赖的第三方软件

Redis

##说明

本程序用flask作为web容器，接到作业后交给celery异步处理，可以通过查询状态获取作业的完成情况。Redis用作celery的broker。前端用了semantic-ui和jQuery库。

仅脚本查询的话，只需要安装requests、pycrypto两个python库，将`wifimasterkey_macos.py`稍微改下即可。

程序搞这么复杂其实只是想练练手而已，学习下任务队列的使用。

###mac osx

执行`airport -s`,将结果粘贴进去
如果提示没有`airport`，先执行
`sudo ln -s /System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport /usr/sbin/airport`

###windows

powershell或者cmd执行`netsh wlan show network mode=bssid`,将结果粘贴进去

## 联系方式

http://5alt.me

md5_salt [AT] qq.com

##参考资料

http://drops.wooyun.org/tips/6049

http://www.wooyun.org/bugs/wooyun-2015-099268

http://drops.wooyun.org/papers/4976
