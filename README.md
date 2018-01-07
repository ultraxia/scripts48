# scripts48


## 简介
Python初学者,微博ID:[沉迷学习的奥特虾](https://weibo.com/5510932216/profile?rightmod=1&wvr=6&mod=personinfo)
饭偶像期间写的一些小程序

## 功能介绍
` 	weiboStory.py`
* 用于查询某一用户所发布的微博故事链接
* 视频文件可直接使用PC浏览器打开右键另存为
* 手机端默认下载.bin后缀文件，需要手动将后缀名修改为.mp4方可播放  
* 所需参数:微博UID

 
`serverMonitor.py`
* 用于监测服务器运行状态
* 可手动修改时间间隔，每隔一段时间向指定QQ群发送Linux服务器CPU和内存使用率
* 若指定时间没有收到推送，则说明QQBot服务意外退出  


`amountTime.py`
* 用于查询某一时间节点集资数目符合设定金额标准的用户ID
* 所需参数：
   - 摩点项目ID
   - 指定金额，支持int型和float型
   - 指定时间，格式为*%Y-%m-%d %H:%M:%S*
 


##  更新记录


**2018.01.07更新**：修复了`weiboStory.py`在多条记录场景下只能显示第一条的BUG

**2018.01.07更新**：新增`amountTime.py`

