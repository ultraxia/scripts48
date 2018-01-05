import psutil
import requests
from qqbot import qqbotsched

groupid = '木里实验室'

@qqbotsched(hour='0-23/2')
def monitorTask(bot):
        gl = bot.List('group', groupid)
        if gl is not None:
                for group in gl:
                        msg = '服务器当前状态：'+'\n'
                        cpu_msg = 'CPU负载：'+str(psutil.cpu_percent(0))+'%'+'\n'
                        mem_msg = '内存已使用：'+str(psutil.virtual_memory()[2])+'%'+'\n'
                        pids = psutil.pids()
                        for pid in pids:
                                p = psutil.Process(pid)
                                if p.name() == 'qqbot':
                                        if len(p.cmdline()) != 4:
                                                status = 'QQBOT:'+p.status().upper()
                        msg = msg+cpu_msg+mem_msg+status
                        bot.SendTo(group, msg)
