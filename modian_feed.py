import random
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

def getOrders(pro_id):
	# print('正在获取集资数据.....'+'\n')
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
		for data in datas:
			print(data)


if __name__ == '__main__':
	print('Copyright (c) 2018 SNH48-费沁源应援会\nPowered by 奥特虾\n')
	pro_id = 12767
	getOrders(pro_id)
	os.system('pause')

	
	
		
