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
   - 指定时间，格式为*%m-%d %H:%M*
   - 指定抽奖人数

`weiboBroadcast.py`
* 用于将指定成员微博内容搬运至群内
* 所需参数：
  - idolName 成员名称
  - groupid 群名称
  - weibo_id 微博UID


`timedBroadcast.py`
* 用于每天晚上定时向群内播报当天集资情况
* 所需参数:
  - proid 摩点项目ID
  - groupid 群名称

`pocket`

`csvout.py`
* 将摩点集资数据以csv格式保存至本地
* 所需参数:
  - proid 摩点项目ID 

`dataCompensation.py`
* 每隔一段时间检查本地数据库与摩点接口返回数据是否一致，自动补偿遗漏数据
* 所需参数:
  - proid 摩点项目ID
  - 数据库相关参数

`saveOrders.py`
* 将摩点订单数据存至数据库
* 所需参数:
  - proid 摩点项目ID
  - 数据库相关参数

`modian_feed.py`
* 显示摩点orders接口返回的信息流
* 所需参数:
  - proid 摩点项目ID

`modian_monitor.py`
* 实时将摩点新产生的订单存至数据库
* 所需参数:
  - proid 摩点项目ID
  - 数据库相关参数

`jzdaily.py`
* 每天晚上定时将当日集资数据存至数据库，分别为总额、参与人数、生成订单数三个维度
* 所需参数:
  - proid 摩点项目ID
  - 数据库相关参数

##  更新记录


**2018.01.07更新**：修复了`weiboStory.py`在多条记录场景下只能显示第一条的BUG

**2018.01.07更新**：新增`amountTime.py`

**2018.01.27更新**：新增`weiboBroadcast.py`

**2018.01.31更新**：对`amountTime.py`进行功能升级和交互优化，现已支持查询指定时间段内集资总额

**2018.02.02更新**：新增`timedBroadcast.py`

**2018.02.07更新**：优化`timedBroadcast.py`，新增涨幅（降幅）提示

**2018.02.07更新**：新增文件夹`pocket`时间胶囊，包含全量备份及增量备份两个脚本

**2018.02.08更新**：优化`amountTime.py`代码逻辑，提升了运行速度，并新增抽奖功能

**2018.03.05更新**：新增`csvout.py`，一键生成集资报表

**2018.04.01更新**：针对摩点orders接口升级，`csvout.py`新增Nonetype数据类型判断

**2018.04.01更新**：新增`dataCompensation.py`、`saveOrders.py`、`modian_feed.py`、`modian_monitor.py`、`jzdaily.py`
`
##一些说明
以上代码均基于[SNH48-费沁源应援会](https://weibo.com/u/5577610720?topnav=1&wvr=6&topsug=1)实际业务需求开发，如果能帮到您，不甚荣幸。同时，由于本人编码能力有限，如不知道如何使用或者有更好的意见，欢迎提交[issues](https://github.com/ultraxia/scripts48/issues)，看到会第一时间处理，感谢关注。
