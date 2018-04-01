#copyright (c) 2018 奥特虾
import random
import requests
import json
import time
import urllib
import hashlib
import datetime
import pymysql



numList= []
moneyList = []
orderList = []

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
		if datas is None:
			break
		date = datetime.datetime.now().strftime('%Y-%m-%d')
		for data in datas:
			if date in data['pay_time']:
				orderList.append(data)
				moneyList.append(data['backer_money'])
				numList.append(data['nickname'])
	moneyNum = '%.2f' % sum(moneyList)
	peopleNum = len(list(set(numList)))
	orderNum = len(orderList)
	save_to_database(date,moneyNum,peopleNum,orderNum)

def save_to_database(date,moneyNum,peopleNum,orderNum):
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("INSERT INTO jzdaily VALUES (%s,%s,%s,%s)", (date,moneyNum,peopleNum,orderNum))
    db.commit()
    db.close()


if __name__ == '__main__':
	pro_id = 12767
	getOrders(pro_id)
	
