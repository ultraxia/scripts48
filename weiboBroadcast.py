# -*- coding: utf-8 -*-
import re
import requests
from qqbot import qqbotsched
import copy
import time


global weibo_id_array
global firstcheck_weibo

weibo_id_array = []
firstcheck_weibo = 1

# ---------------------------------设置项---------------------------------
def idolName():
    idolName = '林歆源'
    return idolName

def groupid():
    groupid = '木里实验室'
    return groupid

# containnerID所在行无需修改
def weibo_id():
    weiboID = '6261962223' 
    containnerID = '107603'+ str(weiboID)            
    return containnerID

# ---------------------------------以下内容无需更改------------------------



# 定时任务。每分钟获取一次微博数据，如果有新的微博，自动发送到群。
@qqbotsched(hour='0-23', minute='0-59/1')
def mytask3(bot):
    global weibo_id_array
    global firstcheck_weibo
    wbcontent = ""
    gl = bot.List('group', groupid())
    if gl is not None:
        for group in gl:
            idcount = -1
            if (firstcheck_weibo == 1):
                weibo_id_array = copy.copy(getidarray())
                firstcheck_weibo = 0
            checkwbid = copy.copy(get_5_idarray())
            if (firstcheck_weibo == 0):
                for cardid in checkwbid:
                    idcount += 1
                    if int(cardid) == 0:
                        continue
                    if cardid not in weibo_id_array:
                        weibo_id_array.append(cardid)
                        retweet = checkretweet(idcount)
                        wbpic = checkpic(idcount)
                        wbscheme = getscheme(idcount)
                        if (retweet):
                            wbcontent = str(idolName())+"刚刚[转发]了一条微博：" + '\n' + '\n' + getretweetweibo(idcount) + '\n'
                            wbcontent = wbcontent + '\n' + "传送门：" + wbscheme
                        else:
                            wbcontent = str(idolName())+"刚刚发了一条新微博：" + '\n' + '\n' + getweibo(idcount) + '\n'
                            if (wbpic):
                                wbcontent = wbcontent + getpic(idcount)
                            wbcontent = wbcontent + '\n' + "传送门：" + wbscheme
                        bot.SendTo(group, wbcontent)



def weibo_url():
    weiboURL = 'https://m.weibo.cn/api/container/getIndex?containerid='+str(weibo_id())
    return weiboURL
    
def dr_to_dd(dr_str):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', dr_str)
    return str(dd)

def init():
    ajax_url = str(weibo_url())
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'}

    form = {
        'containerid': int(weibo_id()),
    }

    response = requests.post(ajax_url, form, headers=header).json()
    return response


def getdata(i):
    response = copy.copy(init())
    datas = response['data']['cards'][i]
    return datas


def checkid(i):
    datas = getdata(i)
    return str(datas['mblog']['id'])


def checkretweet(i):
    datas = getdata(i)
    if datas['mblog'].get('retweeted_status') is None:
        return False
    else:
        return True


def getweibo(i):
    datas = getdata(i)
    r_weibo = str(datas['mblog']['text'])
    r2d_weibo = dr_to_dd(r_weibo)
    return r2d_weibo


def getretweetweibo(i):
    datas = getdata(i)
    r_retweeetweibo = str(datas['mblog']['raw_text'])
    r2d_retweeetweibo = dr_to_dd(r_retweeetweibo)
    return r2d_retweeetweibo


def checkpic(i):
    datas = getdata(i)
    if datas['mblog'].get('pics') is None:
        return False
    else:
        return True


def getpic(i):
    datas = getdata(i)
    picurl = ""
    picnum = 1
    for pic in datas['mblog']['pics']:
        picurl = picurl + "微博配图" + str(picnum) + "：" + str(pic['url']) + '\n'
        picnum += 1
    return picurl


def getscheme(i):
    datas = getdata(i)
    return str(datas['scheme'])


def getidarray():
    weibo_id_array = []
    response = copy.copy(init())
    cards = response['data']['cards']
    for card in cards:
        try:
            weibo_id = card['mblog']['id']
        except Exception as e:
            weibo_id_array.append("0")
        else:
            weibo_id_array.append(weibo_id)
    return weibo_id_array


def get_5_idarray():
    weibo_id_array = []
    response = copy.copy(init())
    cards = response['data']['cards']
    for i in range(0, 5):
        datas = cards[i]
        try:
            weibo_id = datas['mblog']['id']
        except Exception as e:
            weibo_id_array.append("0")
        else:
            weibo_id_array.append(weibo_id)
    return weibo_id_array


