# -*- coding: utf-8 -*-
import requests
import pymysql
import math
import json
import time
import os
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


token = 'IDMf59H3NNATZle2zW8gF2QryBI348MUYRlX8dszJK+Yyw+zL/GJAA=='
roomId = 9339537

mysql_conn = {
        'host': 'localhost',
        'port': 3306,
        'user': 'root',
        'password': '*******',
        'db': 'SNH48',
        'charset': 'utf8'
    }
db = pymysql.connect(**mysql_conn)
cursor = db.cursor()
sql = """CREATE TABLE IF NOT EXISTS lxyPocket(
            senderName varchar(255) NOT NULL,
            msgTime varchar(255) NOT NULL,
            msgTimeStr datetime NOT NULL,
            msgText varchar(255) ,
            imgUrl varchar(255) )
            engine=innodb  default charset=utf8"""
cursor.execute(sql)

ajax_url = 'https://pjuju.48.cn/imsystem/api/im/v1/member/room/message/mainpage'
header = {
    'Host': 'pjuju.48.cn',
    'version': '5.0.1',
    'os': 'android',
    'Accept-Encoding': 'gzip',
    'IMEI': '866716037825810',
    'User-Agent': 'Mobile_Pocket',
    'Content-Length': '67',
    'Connection': 'Keep-Alive',
    'Content-Type': 'application/json;charset=utf-8',
    'token': token
}
form = {
    "lastTime": 0,
    "limit": 10,
    "chatType": 0,
    "roomId": roomId
}
while True:
    response = requests.post(
        ajax_url,
        data=json.dumps(form),
        headers=header,
        verify=False,
    ).json()
    if response['status'] == 200:
        if response['content']['data']:
            datas = response['content']['data']
            lastTime = datas[-1]['msgTime']
            form['lastTime'] = lastTime 
            for data in datas:
                extInfo = json.loads(data['extInfo'])
                senderName = extInfo['senderName']
                msgTime = data['msgTime']
                msgTimeStr = data['msgTimeStr']
                if data['msgType'] == 0:
                    try:
                        text = extInfo['messageText']
                    except:
                        text = extInfo['text'] 
                    cursor.execute("INSERT INTO lxyPocket (senderName,msgTimeStr,msgTime,msgText) VALUES (%s,%s,%s,%s)", (senderName,msgTimeStr,msgTime,text))
                    db.commit()     
                    print(senderName,msgTimeStr,text)
                if data['msgType'] == 1:
                    imgInfo = json.loads(data['bodys'])
                    img = imgInfo['url']
                    cursor.execute("INSERT INTO lxyPocket (senderName,msgTimeStr,msgTime,imgUrl) VALUES (%s,%s,%s,%s)", (senderName,msgTimeStr,msgTime,img))
                    db.commit()
                    print(senderName,msgTimeStr,img)
        else:
            print('finish')
            break
    
    time.sleep(3)




