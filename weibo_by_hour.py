# -*- coding: utf-8 -*-
"""
File Name：     main
Description :
Author :       meng_zhihao
mail :       312141830@qq.com
date：          2020/2/4
"""

import datetime
import time
from selenium_operate import ChromeOperate
from crawl_tool_for_py3_v6 import crawlerTool as ct
import text_emotion
import random
import json
import pymysql
def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates

def weibo_search():
    start_date = '2020-02-20'
    end_date = '2020-03-17'
    cop = ChromeOperate(executable_path='..\chromedriver.exe')
    date_list = dateRange(start_date, end_date)
    #search_url_template='https://s.weibo.com/weibo/%25E7%25BA%25A2%25E8%2596%25AF%25E5%25A4%25AB%25E5%25A6%2587?q=新冠肺炎&scope=ori&typeall=1&suball=1&timescope=custom:{0}-0:{1}-0&Refer=g'
    print(date_list)
    search_url_template =  'https://s.weibo.com/weibo?q=新冠疫情&typeall=1&suball=1&timescope=custom:{0}-{1}:{2}-{3}&Refer=g'
   #‘https://s.weibo.com/weibo/7%25E5%25A4%25B4%25E8%25A2%25AB%25E6%259A%2582%25E5%2585%25BB%25E7%259A%2584%25E6%2590%2581%25E6%25B5%2585%25E7%2593%259C%25E5%25A4%25B4%25E9%25B2%25B8%25E7%258E%25B0%25E7%258A%25B6?q=%E6%96%B0%E5%86%A0%E8%82%BA%E7%82%8E&typeall=1&suball=1&timescope=custom:2020-01-13:2020-02-20&Refer=g    line = ['时间', '博文id','用户', '用户id', '评论', '转发', '点赞', '博文','情感分数']
    line = ['时间', '博文id', '用户', '用户id', '评论', '转发', '点赞', '博文', '情感分数']
    hours=[
        [0,2],
        [2, 4],
        [4, 6],
        [6, 8],
        [8, 10],
        [10, 12],
        [12, 14],
        [14, 16],
        [16, 18],
        [18, 20],
        [20, 22],
        [22, 23]
    ]
    yield line
    for i in range(len(date_list)-1):
        for hour in hours:
            start_date = date_list[i]
            end_date = date_list[i+1]
            print(start_date)
            shour,ehour = hour[0],hour[1]
            search_url = search_url_template.format(start_date,shour,start_date,ehour)
            cop.open(search_url)
            for page_num in range(5):
                try:
                    page_buf = cop.open_source()
                    posts = ct.getXpath('//div[@class="card-wrap"]',page_buf)
                    for post in posts:
                        texts = ct.getXpath('//p[@node-type="feed_list_content_full"]//text()',post)
                        if not texts:
                            texts = ct.getXpath('//p[@node-type="feed_list_content"]//text()', post)
                        texts = ''.join(texts)
                        sentiScore = text_emotion.get_sentiment_score(texts)
                        if not texts:
                            continue
                        date = ""
                        from_source = ct.getXpath('//p[@class="from"]',post)
                        if from_source:
                            date = ct.getXpath1('//a/text()', from_source[-1])
                            date = date.strip()
                        nick = ct.getXpath1('//a/@nick-name',post)
                        user_id =  ct.getXpath1('//a[@class="name"]/@href',post)
                        user_id = ct.getRegex('weibo.com/(\d+)',user_id)
                        mid = ct.getXpath1('//div/@mid',post)
                        ''
                        # 评论
                        comments_button = ct.getXpath1('//a[@action-type="feed_list_comment"]/text()',post)
                        comments_count = ct.getRegex('评论 (\d+.*)', comments_button)
                        if not comments_count:
                            comments_count = 0
                        # get_comments = []
                        feed_list_forward_button = ct.getXpath1('//a[@action-type="feed_list_forward"]/text()', post)
                        forward_count = ct.getRegex('转发 (\d+.*)', feed_list_forward_button)
                        if not forward_count:
                            forward_count=0

                        like_button = ct.getXpath('//a[@action-type="feed_list_like"]', post)
                        if like_button:
                            like_button =like_button[-1]
                            like_button = ct.getXpath1("//em/text()",like_button)
                            like_count = ct.getRegex('(\d+.*)', like_button)
                            if not like_count:
                                like_count = 0
                        else:
                            like_count = 0

                        # feed_list_forward  # 转发

                        # if ct.getRegex('评论 (\d+.*)',comments_button):
                        #                     #     try:
                        #                     #         # proxy = ct.get_new_1min_proxy()
                        #                     #         # proxies = {'http': 'http://' + proxy, 'https': 'http://' + proxy}
                        #                     #         # try:
                        #                     #         #     comments_page = ct.get('https://m.weibo.cn/api/comments/show?id='+mid,proxies=proxies) # 获取评论会封ip，另外有很多评论不可见(敏感词，用户设置) 虽然评论数不是空
                        #                     #         # except:
                        #                     #         #     time.sleep(2)
                        #                     #         time.sleep(2)
                        #                     #         comments_page = ct.get('https://m.weibo.cn/api/comments/show?id=' + mid)
                        #                     #         json_data = json.loads(comments_page)
                        #                     #         comments = json_data['data']['data']
                        #                     #         for comment in comments:
                        #                     #             comment_text = comment['text']
                        #                     #             get_comments.append(comment_text)
                        #                     #     except Exception as e:
                        #                     #         print(e,mid)
                        #连接mysql
                        # conn = pymysql.connect(host='localhost',user='root',password='mysql',database='mysql')
                        # cur = conn.cursor()#设置游标
                        # sql = 'insert into sheet1(时间, 博文id, 用户, 用户id, 评论, 转发, 点赞, 博文, 情感分数,转评赞) values (%s, %s , %s, %s, %s, %s, %s, %s, %s, %s)'''(date,mid,nick,user_id,comments_count,forward_count,like_count,texts,sentiScore,counts)
                        # try:
                        #     cur.execute(sql)
                        #     conn.commit()
                        # except:
                        #     cur.rollback()
                        #     print('写入失败')
                        # cur.close()
                        # conn.close()

                        line = [date,mid,nick,user_id,comments_count,forward_count,like_count,texts,sentiScore]
                        yield line

                    next_button = cop.find_elements_by_xpath('//a[@class="next"]')
                    if next_button:
                        time.sleep(random.randint(2, 4))
                        next_button[0].click()
                    else:
                        break
                except Exception as e:
                    print(e)


if __name__ == '__main__':
    data = weibo_search()
    ct.writer_to_csv(data, 'outputs/phase3新冠疫情.csv')

