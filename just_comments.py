# -*- coding: utf-8 -*-
"""
File Name：     just_comments
Description :
Author :       meng_zhihao
mail :       312141830@qq.com
date：          2020/2/11
"""
from selenium_operate import ChromeOperate
import pandas as pd
from crawl_tool_for_py3_v6 import crawlerTool as ct
import time
# data=[]
# def  get_url(path):
# 	with open(path,'r') as f:
# 		wb_url=f.readlines()
# 		# user_id=np.char.rstrip(user_list,'\n')
# 		return wb_url
def main():
    cop = ChromeOperate(executable_path=r'D:\chromedownload\anaconda\chromedriver.exe')
    # for wb_url in get_url('./input file/wbURL'):
    url = 'https://m.weibo.cn/status/4619438161398837'
    cop.open(url)
    while True:
        time.sleep(1)
        cop.down_page()
        page_buf = cop.open_source()
        comments = ct.getXpath('//h3/text()', page_buf)
        comments = [[text] for text in comments]
        ct.writer_to_csv(comments, 'comments.csv')
if __name__ == '__main__':
    main()