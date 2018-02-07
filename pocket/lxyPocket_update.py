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

def connect_db():
    mysql_conn = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '*****',
            'db': 'SNH48',
            'charset': 'utf8'
        }
    db = pymysql.connect(**mysql_conn)
    return db

def querry_time():
    times = (time.time()-3600)*1000
    return times


def main():
    db = connect_db()
    cursor = db.cursor()
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

    a = True
    while a:
        response = requests.post(
            ajax_url,
            data=json.dumps(form),
            headers=header,
            verify=False,
        ).json()

        datas = response['content']['data']
        lastTime = datas[-1]['msgTime']
        form['lastTime'] = lastTime 
        for data in datas:
            if data['msgTime'] > int(querry_time()):
                extInfo = json.loads(data['extInfo'])
                senderName = extInfo['senderName']
                msgTimeStr = data['msgTimeStr']
                msgTime = data['msgTime']
                if data['msgType'] == 0:
                    try:
                        text = extInfo['messageText']
                    except:
                        text = extInfo['text'] 
                    cursor.execute("INSERT INTO lxyPocket (senderName,msgTime,msgTimeStr,msgText) VALUES (%s,%s,%s,%s)", (senderName,msgTime,msgTimeStr,text))
                    db.commit()
                if data['msgType'] == 1:
                    imgInfo = json.loads(data['bodys'])
                    img = imgInfo['url']
                    cursor.execute("INSERT INTO lxyPocket (senderName,msgTime,msgTimeStr,imgUrl) VALUES (%s,%s,%s,%s)", (senderName,msgTime,msgTimeStr,img))
                    db.commit()
            else:
                print('Finish')
                break
        a = False
        time.sleep(3)

if __name__ == '__main__':
    main()




