import setting
import requests
import json
import urllib
import hashlib
import time
import datetime
from qqbot import qqbotsched


#-----------------------------设置项-----------------------
#设置摩点pro_id
proid = 10703
#设置群名称
groupid = '费沁源的冰糖草莓们'
#----------------------------------------------------------

money_list = []
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

#此处设置定时播报的时间
@qqbotsched(hour='23', minute='59')
def mytask3(bot):
    gl = bot.List('group', groupid)
    if gl is not None:
        for group in gl:
            bot.SendTo(group,timing_querry())


def Time_format_conversion(dt):
    timeStamp = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")) 
    return timeStamp

def getSign(ret):
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign

def timing_querry():
    endTime = time.time()
    startTime = endTime-86400
    page = 1
    url = 'https://wds.modian.com/api/project/orders'
    while True:
        form = {
            'page': page,
            'pro_id': proid
        }
        sign = getSign(form)
        form['sign'] = sign
        response = requests.post(url, form, headers=header).json()
        page +=1
        datas = response['data']
        for data in datas:
            orderTime = Time_format_conversion(data['pay_time'])
            if startTime <= orderTime <= endTime:
                money_list.append(float(data['backer_money']))
        if datas == []:

            break

#发送内容可自定义
    msg = '美好的一天快要结束啦，今天冰糖草莓们累计达成了%.2f元集资，再接再厉哟~' % sum(money_list)
    return msg
