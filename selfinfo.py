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
header={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'cookie':'_T_WM=adee6437b7d653ec43264766859ba917; SCF=AqnM8hD115DWl_TMp9FNky0f2VWBtfn1el-8Z1I7YSxZhfIVKNH0d_ihg7-LcquVK6wSWJBq4H5GhZQOYi62lck.; SUB=_2A25N79ipDeRhGeNH7VQZ-CvJzjiIHXVvE_jhrDV6PUJbktB-LUrRkW1NSoIhiJvtTiZv9d9UxrDLZz_Jl6wZXnh6; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhlS0YnVFOJS1y.m-RpciCC5NHD95Qf1Kqc1hnfSK-XWs4Dqcjdi--RiK.Ni-2Xi--Xi-iWiK.fi--RiKyWiKyF; SSOLoginState=1626056953',
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
for user_id in get_id('./input file/userlist.csv'):
    try:
        url=url_new+user_id
        r_text=gethtml(url,header)
        html=etree.HTML(r_text.encode('utf-8'))
        user_name=html.xpath('//span[@class="ctt"]/text()')[0]
        inf=html.xpath('//span[@class="ctt"][1]/text()')
        weibo_number=html.xpath('//div[@class="tip2"]/span[@class="tc"]/text()')[0].replace('微博','').strip('[]')
        focus_number=html.xpath('//div[@class="tip2"]/a[1]/text()')[0].replace('关注','').strip('[]')
        fan_number=html.xpath('//div[@class="tip2"]/a[2]/text()')[0].replace('粉丝','').strip('[]')
        uid = user_id.rstrip()#去除空格
        url_info = 'https://weibo.cn/%s/info' % str(uid)
        htmltext=gethtml(url_info,header)
        html1=etree.HTML(htmltext.encode('utf-8'))
        level = html1.xpath("/html/body/div[4]/text()[1]")[0].replace('会员等级:', '').strip('[]')
        verified = html1.xpath("/html/body/div[6]/text()[6]")[0].strip('[]')#.replace('认证:','')
        # user_info=user_basic+user_id+'/info'
        # u_text=gethtml(user_info,header)
        # html1=etree.HTML(u_text.encode('utf-8'))
        # level=html1.getXpath('/html/body/div[5]/text()[1]')
        data.append([user_name,inf,weibo_number,focus_number,fan_number,level,verified])
        count+=1
        print('第{}个用户信息写入完毕'.format(count))
        time.sleep(random.randint(1,2))
    except:
        print('用户信息不完全')
df=pd.DataFrame(data,columns=['user_id','inf','weibo_num','focus_num','fans_num','level','verified'])
df.to_csv('weibo_all.csv',index=False,encoding='gb18030')

