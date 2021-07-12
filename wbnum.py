import requests
import random
import re
from selenium_operate import ChromeOperate
from crawl_tool_for_py3_v6 import crawlerTool as ct
import time
import pandas as pd
import numpy as np
import requests
from lxml import etree
import random
import time
header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
       'cookie':'_T_WM=c8562182173ade7507b4697f554a5e5c; SCF=AqnM8hD115DWl_TMp9FNky0f2VWBtfn1el-8Z1I7YSxZHSioj1_xeLQJgRcrnamIzZUrpoL7S_V2zS_0ZA808do.; SUB=_2A25NXaX6DeRhGeNH7VQZ-CvJzjiIHXVuocuyrDV6PUJbktAfLRXXkW1NSoIhiFbLe5Mc2XXu9JABMWgFc0zGU-CQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhlS0YnVFOJS1y.m-RpciCC5NHD95Qf1Kqc1hnfSK-XWs4Dqcjdi--RiK.Ni-2Xi--Xi-iWiK.fi--RiKyWiKyF; _T_WL=1; _WEIBO_UID=5966885554',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
url_new='https://weibo.cn/u/'
user_basic='https://weibo.cn/'
data=[]
count=0
def  get_id(path):
	with open(path,'r') as f:
		user_id=f.readlines()
		# user_id=np.char.rstrip(user_list,'\n')
		return user_id
def gethtml(url,header):
    r=requests.get(url,headers=header)
    if r.status_code==200:
        return r.text
    else:
        print('网络连接异常')
for user_id in get_id('input file/users.csv'):
    try:
        url=url_new+user_id
        print(url)
        r_text = gethtml(url, header)
        html = etree.HTML(r_text.encode('utf-8'))
        fan_number = html.xpath('//div[@class="tip2"]/a[2]/text()')[0].replace('粉丝', '').strip('[]')
        focus_number = html.xpath('//div[@class="tip2"]/a[1]/text()')[0].replace('关注', '').strip('[]')
        weibo_number=html.xpath('//div[@class="tip2"]/span[@class="tc"]/text()')[0].replace('微博','').strip('[]')
        data.append([ user_id,weibo_number,fan_number,focus_number])
        count += 1
        print('第{}个用户信息写入完毕'.format(count))
        time.sleep(random.randint(1, 2))
    except:
        print('用户信息不完全')
df=pd.DataFrame(data,columns=['user_id','weibo_num','fan_number','focus_number'])
df.to_csv('weibo_num.csv',index=False,encoding='gb18030')