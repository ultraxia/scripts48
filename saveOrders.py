import requests
import json
import urllib
import hashlib
import time
import pymysql

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

def connect_database():
    mysql_conn = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'xxxxx',
            'db': 'xxxxx',
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

def getOrders(pro_id):
    page = 1
    while True:
        url = 'https://wds.modian.com/api/project/orders'
        form = {
            'page': page,
            'pro_id': pro_id
        }
        sign = getSign(form)
        form['sign'] = sign
        response = requests.post(url, form, headers=header).json()
        page += 1
        datas = response['data']
        if datas == []:
            break
        for data in datas:
            user_id = data['user_id']
            nickname = data['nickname']
            backer_money = data['backer_money']
            pay_time = data['pay_time']
            print(user_id,nickname,backer_money,pay_time)
            print('正在写入数据')
            db = connect_database()
            cursor = db.cursor()
            cursor.execute("INSERT INTO strawberry VALUES (%s,%s,%s,%s,%s)", (pro_id,user_id,nickname,backer_money,pay_time))
            db.commit()
            print('数据存储完成\n')
            db.close()



if __name__ == '__main__':
    pro_id = 12767
    getOrders(pro_id)
    
