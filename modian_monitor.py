import requests
import json
import urllib
import hashlib
import time
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

def connect_database():
    mysql_conn = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'xxxxxxx',
            'db': 'xxxxxx',
            'charset': 'utf8'
        }
    db = pymysql.connect(**mysql_conn)
    cursor = db.cursor()
    return db

def getSign(ret):
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign

def Time_format_conversion(dt):
    timeStamp = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))
    return timeStamp

def getOrders(pro_id, page):
    url = 'https://wds.modian.com/api/project/orders'
    form = {
        'page': page,
        'pro_id': pro_id
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    return response

def newOrder():
    print('正在发起请求')
    stampTime = int(time.time())
    print('当前时间%s' % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    newOrders = []
    orderDict = getOrders(pro_id, 1)
    for data in orderDict['data']:
        paytimeStamp = Time_format_conversion(data['pay_time'])
        if paytimeStamp >= stampTime - 10 and paytimeStamp < stampTime:
            newOrders.append(data)
    if newOrders:
        print('有新订单产生！\n')
        for newOrder in newOrders:   
            user_id = newOrder['user_id']
            nickname = newOrder['nickname']
            backer_money = newOrder['backer_money']
            pay_time = newOrder['pay_time']
            print(user_id,nickname,backer_money,pay_time)
            print('正在写入数据')
            db = connect_database()
            cursor = db.cursor()
            cursor.execute("INSERT INTO strawberry VALUES (%s,%s,%s,%s,%s)", (pro_id,user_id,nickname,backer_money,pay_time))
            db.commit()
            print('数据存储完成\n')
            db.close()
    else:
        print('暂无新订单产生\n')



if __name__ == '__main__':
    pro_id = 12767
    sched = BlockingScheduler()
    sched.add_job(newOrder, 'interval', seconds=10) 
    sched.start()
