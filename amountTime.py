import requests
import json
import time
import os
import sys
import urllib
import hashlib
import datetime


name_list = []
money_list = []

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

def getSign(ret):
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign

def project_name(pro_id):
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_id
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    project_name = response['data'][0]['pro_name']
    return project_name

def getOrders(pro_id,startTime,endTime,backerStandard):
    print('查询中.....'+'\n')
    page = 1
    url = 'https://wds.modian.com/api/project/orders'
    while True:
        form = {
            'page': page,
            'pro_id': pro_id
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
                if float(data['backer_money']) >= float(backerStandard):
                    name_list.append(data['nickname'])      
        if datas == []:
            break

def Time_format_conversion(dt):
    timeStamp = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")) 
    return timeStamp


def start(name_list):
    year = '2018-'
    sec = ':00'
    pro_id = input('请设置摩点项目ID：')
    start = input('请设置起始时间：')
    startTime = Time_format_conversion(year+start+sec)
    end = input('请设置结束时间：(默认将以当前时间计算)')   
    if end == '':
        endTime = time.time()
    else:
        endTime = Time_format_conversion(year+end+sec)
    backerStandard = input('请设置金额:(可跳过)')
    
    if backerStandard == '':
        backerStandard = 0
        getOrders(pro_id,startTime,endTime,backerStandard)
        print('设定时间段内累计达成集资%.2f元' % sum(money_list))
    else:
        getOrders(pro_id,startTime,endTime,backerStandard)
        name_list = list(set(name_list))
        print('在'+str(project_name(pro_id))+'中,'+str(start)+'后集资'+str(backerStandard)+'元以上共有'+str(len(name_list))+'人'+'\n')
    
        for ID in name_list:
            print(ID+'\n')

        

if __name__ == '__main__':
    print('Copyright (c) 2018 SNH48-费沁源应援会\nPowered by 奥特虾\n')
    time.sleep(1.5)
    start(name_list)
    os.system('pause')

    
    
        

