## CUMT多线程公选课抢课脚本

**Demo**
![](https://upload-images.jianshu.io/upload_images/11356161-9d4ba3a89d6d8637.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

***

**How To Use**

+ 安装依赖包：`pip install -r requirements.txt`

+ 下载本仓库文件与[CUMT教务系统模拟登录](https://github.com/EddieIvan01/Analog_Login)文件置于与同一文件夹下

+ 修改config.json，填入教务系统用户名，密码，与欲选课程代号，
e.g.

![](https://upload-images.jianshu.io/upload_images/11356161-7009588876ac3fad.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

+ 启动程序，输入启动的线程数。设定只能小于8（为学校的土豆服务器考虑）

+ 长时间暴力发送请求很可能会被教务系统服务器ban掉IP，暂时没有写代理功能，被ban了就换个网继续吧...

+ INFO中的请求成功指请求服务器成功并接收响应成功，正常状态下会一直看到`请求成功`和`异常`

+ 解释状态码：
   
  + `1,6D410DC519E6029AE053C0A86D5CEAA6,100,0`为课程无余量
   
  + 其余状态码都是中文如`课程时间冲突`
  
+ 仅支持搜索搜索课程代号只有一个结果的课程

***

对于无余量的课程，可以挂在电脑上，持续监控，大概是这样的画面

![](https://upload-images.jianshu.io/upload_images/11356161-96e12173538f401a.gif?imageMogr2/auto-orient/strip)

如果有服务器可以使用nohup指令挂载到服务器上，`nohup ./rob.py&`

***

P.s. 部分post变量代号还不清楚，程序可能不具有不同学院不同年级的普适性。如有疑问，请联系whoami9894@gmail.com

***

2018/7/8 16.26   长时间监控时Cookie过期问题已修复

2018/7/8 20.34   发现校园网及移动宽带会出现获取课程信息失败，服务器会返回400 Bad Request（大概是玄学），CSDN上有[同样的问题](https://bbs.csdn.net/topics/390131855)，可能是ISP线路问题导致丢包，但是浏览器访问是好好的。联通流量网络正常。东京的VPS也失败。

2018/7/8 23.58   已打包成exe文件，使用时将`config.json`与rob.exe放于同一文件夹下，启动exe文件即可
