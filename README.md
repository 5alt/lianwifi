#wifi万能钥匙网页版

##简介

脚本会开启http服务，模拟mac版wifi万能钥匙进行wifi密码的查询

查询页面：

`http://<hosthost>:<port>/wifi`

提示查询过于频繁，更新认证信息：

`http://<hosthost>:<port>/refresh`

如有侵权，请联系作者删除代码

基于WiFi万能钥匙Mac客户端V1.1.0版开发（ 更新日期：2014-07-22）

##依赖的python库

```
sudo pip install flask
sudo pip install requests
sudo pip install pycrypto
```

## 联系方式

http://5alt.me

md5_salt [AT] qq.com

##参考资料

http://drops.wooyun.org/tips/6049

http://www.wooyun.org/bugs/wooyun-2015-099268

http://drops.wooyun.org/papers/4976
