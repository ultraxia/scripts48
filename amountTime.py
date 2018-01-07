import requests
import json
import time
import os
import sys
import urllib
import hashlib


name_list = []

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}


# 计算签名
def getSign(ret):
    # 将字典按键升序排列，返回一个元组tuple
    tuple = sorted(ret.items(), key=lambda e: e[0], reverse=False)
    md5_string = urllib.parse.urlencode(tuple).encode(encoding='utf_8', errors='strict')
    md5_string += b'&p=das41aq6'
    # md5计算 & 十六进制转化 & 根据规则从第6位开始取16位
    sign = hashlib.md5(md5_string).hexdigest()[5: 21]
    return sign

def project_name():
	url = 'https://wds.modian.com/api/project/detail'
	form = {
        'pro_id': pro_id
	}
	sign = getSign(form)
	form['sign'] = sign
	response = requests.post(url, form, headers=header).json()
	project_name = response['data'][0]['pro_name']
	return project_name

def getOrders():
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
			timestamp = time.mktime(time.strptime(data['pay_time'], "%Y-%m-%d %H:%M:%S"))
			if timestamp >= timestandard:
				if float(data['backer_money']) >= float(backerStandard):
					name_list.append(data['nickname'])		
		if datas == []:
			break
	

if __name__ == '__main__':
	pro_id = input('请输入摩点项目ID：')
	dt = input('请输入时间：')
	timestandard = time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S"))
	backerStandard = input('请输入金额：')
	print('查询中.....'+'\n')
	getOrders()
	name_list = list(set(name_list))
	print('在'+str(project_name())+'中,'+dt+'后集资'+backerStandard+'元以上共有'+str(len(name_list))+'人'+'\n')
	for ID in name_list:
		print(ID)
	print('\n'+'Powered by Ultraxia')
	os.system('pause')
		

