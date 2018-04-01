# Copyright (c) 2018 奥特虾
import requests
import json
import time
import urllib
import hashlib
import datetime
import pymysql

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

payTimeList = []

def connect_database():
    mysql_conn = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'xxxxxx',
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

def querry_database():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT SUM(backer_money) FROM strawberry")
    results = cursor.fetchall()
    for row in results:
    	dbMoney = row[0]
    	return dbMoney

def querry_payTime():
    db = connect_database()
    cursor = db.cursor()
    cursor.execute("SELECT pay_time FROM strawberry WHERE DATE_FORMAT(pay_time,'%m-%d') = DATE_FORMAT(now(),'%m-%d')")
    results = cursor.fetchall()
    for row in results:
    	payTime = str(row[0])
    	payTimeList.append(payTime)

def getDetail():
    url = 'https://wds.modian.com/api/project/detail'
    form = {
        'pro_id': pro_id
    }
    sign = getSign(form)
    form['sign'] = sign
    response = requests.post(url, form, headers=header).json()
    already_raised = response['data'][0]['already_raised']
    return already_raised

def getOrders():
	page = 1
	url = 'https://wds.modian.com/api/project/orders'
	a = True
	while a:
		form = {
	        'page': page,
	        'pro_id': pro_id
		}
		sign = getSign(form)
		form['sign'] = sign
		response = requests.post(url, form, headers=header).json()
		page +=1
		datas = response['data']
		date = datetime.datetime.now().strftime('%Y-%m-%d')
		for data in datas:
			if date in data['pay_time']:
				if data['pay_time'] not in payTimeList:
					user_id = data['user_id']
					nickname = data['nickname']
					backer_money = data['backer_money']
					pay_time = data['pay_time']
					db = connect_database()
					cursor = db.cursor()
					cursor.execute("INSERT INTO dataCompensation VALUES (%s,%s,%s,%s,%s)", (pro_id,user_id,nickname,backer_money,pay_time))
					db.commit()
					msg = str(time.strftime("%a %b %d %H:%M:%S", time.localtime())) + '  '+ \
					'[WARMING] 发现遗漏订单,数据补偿机制启动   ' + \
					str(user_id)+'  '+nickname+'  '+str(backer_money)+'  '+str(pay_time)
					print(msg)
					with open('/var/log/dataCompensation.log', 'a+') as f:
						f.write(msg)
				else:
					a = False
			else:
				msg = str(time.strftime("%a %b %d %H:%M:%S", time.localtime())) + '  '+ \
					'[ERROR] 数据异常，请及时检查'
				a = False
		with open('/var/log/dataCompensation.log', 'a+') as f:
			f.write(msg)
		print(msg)

def main():
	querry_payTime()
	if getDetail() != querry_database():
		getOrders()
	else:
		msg = str(time.strftime("%a %b %d %H:%M:%S", time.localtime())) + '  '+ \
					'[INFO] 例行巡检完成，未发现遗漏订单'
		with open('/var/log/dataCompensation.log', 'a+') as f:
			f.write()
		print(msg)
if __name__ == '__main__':
    pro_id = 12767
    main()


