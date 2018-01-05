from qqbot import qqbotsched
import requests
import json
    
def onQQMessage(bot, contact, member, content):
	global chatdetail
	if contact.ctype == 'group':
		if '微博故事：' in content :
			weiboStory(bot, contact, member, content)  

def weiboStory(bot, contact, member, content):
	gl = bot.List('group', '费沁源的冰糖草莓们')
	if gl is not None:
		for group in gl:
			uid = content[5:]
			if uid == '费沁源':
				uid = '5680343342'
			elif uid == '林歆源':
				uid = '6261962223'
			else:
				uid = content[5:]             
			ajax_url = 'http://api.weibo.cn/2/stories/details?networktype=wifi&extprops=%7B%7D&moduleID=715&checktoken=9bd0b9b6c68c4e56eaaf87785a8e54de&wb_version=3534&c=android&i=0c5de77&s=36d35af7&ft=0&ua=samsung-SM-G9280__weibo__8.0.0__android__android6.0.1&wm=2468_1001&aid=01AqGaR6eqrXXb-RGQqRwx7FjXVNsz3fIQXQdZCRBXJdLOXtw.&did=5e9133bfa983c1e3ec71f919622900c5d0f65bbe&v_f=2&v_p=56&from=1080095010&gsid=_2AkMtUkyOf8NhqwJRmPEUxG7gbIV1wgjEieKbDr1VJRMxHRl-wT9kqnEdtRVeaZfxp96iLZpKqNP_iHhzLbUHuw..&lang=zh_CN&skin=default&type=4&oldwm=4209_8001&sflag=1&story_ids='+str(uid)+'_0'
			data = requests.get(ajax_url).json()
			idolName = data['story_details'][0]['story']['owner']['nickname']
			page = 0
			msg = str(idolName)+'的微博故事链接为：'+'\n'
			while True:
				try:
					storyUrl = data['story_details'][0]['story']['segments'][page]['resources'][0]['hd_url']
					page = page+1
					msg = msg+storyUrl+'\n'
				except:
					break
			bot.SendTo(contact,msg)



