# pocket时间胶囊


## 简介
珍惜当下，且行且珍惜
通过口袋48的API接口，获取指定成员聚聚房间发言记录并存至本地数据库


## 功能介绍
`lxyPocket_save.py`
* 全量备份脚本，运行后将会把所有能够查询到的数据保存至数据库
* 所需参数:
   - token(获取方法可参考[chinsin](https://github.com/ultraxia/qqbot_hzx/blob/master/gettoken.py))
   - roomId([点击获取](https://github.com/chinshin/qqbot_hzx/blob/master/roomID.conf))

`lxyPocket_update.py`
* 增量备份脚本，运行后将获取一小时内产生的更新数据
* 所需参数(同`lxypocket_save.py`)
* 建议结合Linux crontab命令定时执行


 


