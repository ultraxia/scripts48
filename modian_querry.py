import os
import json
import time
import urllib
import random
import hashlib
import threading
import requests
from lxml import etree

moneyList = []



header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) Appl\
eWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

def msg():
    msgList = ['程序飞速运行中，稍安勿躁~','稍等哦，程序运行速度取决于你的网速，让代码飞一会儿']
    return msgList

def userUrl():
    url = 'https://me.modian.com/user?type=backer&id=' + str(user_id)
    return url

def getProid():
    proidList = []
    url = str(userUrl())
    html = requests.get(url).content
    selector = etree.HTML(html)
    infos = selector.xpath('//*[@class="prothumb"]/a[1]')
    for info in infos:
        projectUrl = info.xpath('@href')[0].split('.html')[0]
        proid = projectUrl[34:]
        proidList.append(proid)
    return proidList

def getNickname():
    url = str(userUrl())
    html = requests.get(url).content
    selector = etree.HTML(html)
    infos = selector.xpath('/html/body/div[1]/div[1]/div/div/h5/b')
    for info in infos:
        nickname = info.xpath('text()')[0]
    return nickname

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

def getRankings(pro_id):
    dataList = []
    url = 'https://wds.modian.com/api/project/rankings'
    page = 1
    a = True
    try:
        while a:
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
                nickname = data['nickname']
                if getNickname() == nickname: 
                    moneyList.append(float(data['backer_money']))  
                    projectName = project_name(pro_id)
                    result = '排名：'+str(data['rank'])+'    '+'金额：'+str(data['backer_money'])+'\n\n'
                    msg = projectName+'\n'+result
                    write(msg)
                    a = False
    except TypeError:
        print('检测到一个微打赏项目，本程序无法查询')

def write(msg):
    title = getNickname()+'的水表.txt'
    with open(title, 'a+') as f:
        f.write(msg)

def main():
    print(random.choice(msg())+'\n')
    for pro_id in getProid():
        print(pro_id)
        t = threading.Thread(target=getRankings,args=(pro_id,))
        t.start()

if __name__ == '__main__':
    print('Copyright (c) 2018 SNH48-费沁源应援会\nPowered by 奥特虾\n')
    user_id = input('请输入用户ID：')
    main()

