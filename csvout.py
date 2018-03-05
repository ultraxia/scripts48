import random
import requests
import json
import time
import os
import sys
import urllib
import hashlib
import datetime
import pandas as pd


orderList= []

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

def getOrders(pro_id):
    print('正在获取集资数据.....'+'\n')
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
            orderList.append((data['nickname'],data['backer_money'],data['pay_time']))              
        if datas == []:
            break

def getRankings(pro_id):
    print('正在获取集资数据.....'+'\n')
    page = 1
    while True:
        url = 'https://wds.modian.com/api/project/rankings'
        form = {
            'page': page,
            'pro_id': pro_id,
            'type': 1
        }
        sign = getSign(form)
        form['sign'] = sign
        response = requests.post(url, form, headers=header).json()
        page +=1
        datas = response['data']
        for data in datas:
            orderList.append((data['rank'],data['nickname'],data['backer_money']))
        if datas == []:
            break       

def save_to_csv(type):
    df = pd.DataFrame(orderList)
    if type == '1':
        df.columns = ['rank','ID', 'num']
        filename = '%s.csv' % project_name(pro_id)
    if type == '2':
        df.columns = ['ID', 'num','time']
        filename ='%s明细.csv' % project_name(pro_id)
    df.to_csv(filename, encoding='utf-8', index=False)
    print('csv文件输出完成')
        

if __name__ == '__main__':
    print('Copyright (c) 2018 SNH48-费沁源应援会\nPowered by 奥特虾\n')
    print('\n模式说明：\n模式1为榜单查询模式\n模式2为订单明细查询模式\n')
    pro_id = input('请输入摩点ID:')
    type = input('请输入查询模式：')
    if type == '1':
        getRankings(pro_id)
    if type == '2':
        getOrders(pro_id)   
    save_to_csv(type)
    os.system('pause')
    
    
        

