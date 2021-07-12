import requests
import random
import time
import pandas as pd
import re
class WBcomments(object):
    def __init__(self):
        self.url = 'https://m.weibo.cn/comments/hotflow?'
        self.user_agent = [
            "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
            "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "UCWEB7.0.2.37/28/999",
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
            # iPhone 6：
            "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25",
        ]
        self.headers = {'User-Agent': random.choice(self.user_agent),
                   'Cookie': 'SCF=AqnM8hD115DWl_TMp9FNky0f2VWBtfn1el-8Z1I7YSxZHSioj1_xeLQJgRcrnamIzZUrpoL7S_V2zS_0ZA808do.; SUB=_2A25NXaX6DeRhGeNH7VQZ-CvJzjiIHXVuocuyrDV6PUJbktAfLRXXkW1NSoIhiFbLe5Mc2XXu9JABMWgFc0zGU-CQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhlS0YnVFOJS1y.m-RpciCC5NHD95Qf1Kqc1hnfSK-XWs4Dqcjdi--RiK.Ni-2Xi--Xi-iWiK.fi--RiKyWiKyF; _WEIBO_UID=5966885554; _T_WM=24334246101; XSRF-TOKEN=dd67bd; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4468380427920938%26luicode%3D20000061%26lfid%3D4468631603408517%26uicode%3D20000061%26fid%3D4468380427920938',
                    'Referer': 'https://m.weibo.cn/detail/4497103885505673',
                   'Sec-Fetch-Mode': 'navigate'

                   }

        self.proxies = {
            'http': 'http://118.113.247.115:9999',
            'https': 'https://118.113.247.115:9999'
        }

    params = {}
    list_text = []
    file = './'
#获取每条微博url中的参数
    def processData(self,text):
        text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
        text = re.sub(r"\[\S+\]", "", text)  # 去除表情符号
        # text = re.sub(r"#\S+#", "", text)      # 保留话题内容
        URL_REGEX = re.compile(
            r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
            re.IGNORECASE)
        text = re.sub(URL_REGEX, "", text)  # 去除网址
        text = text.replace("转发微博", "")  # 去除无意义的词语
        text = text.replace('收起全文d', "")
        text = re.sub(r"\s+", " ", text)  # 合并正文中过多的空格
        return text.strip()
    def get_max_id(self):
        response = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        # print(response)
        max_id = response['data']['max_id']
        max_id_type = response['data']['max_id_type']
        data = response['data']['data']
        for i in range(0, len(data)):
            text = data[i]['text']
            label_filter = re.compile(r'</?\w+[^>]*>', re.S)
            text = re.sub(label_filter, '', text)
            text = self.processData(text)
            print(text)
            self.list_text.append(text)

        return max_id, max_id_type#返回元组

    # def run(self,ID):
    #
    #     num_page = 2
    #
    #     # ID = input('请输入你要爬取内容的id：')
    #     # ID = wb_url
    #     return_info = ('0', '0')
    #     for i in range(0, num_page):
    #         print(f'正在爬取第{i + 1}页')
    #         time.sleep(20)
    #         self.params = {
    #             'id': ID,
    #             'mid': ID,
    #             'max_id': return_info[0],
    #             'max_id_type': return_info[1]
    #         }
    #         return_info = self.get_max_id()
    #         data = []
    #         for text in self.list_text:
    #             data.append([ID, text])
    #             df = pd.DataFrame(data, columns=['url', 'comment'])
    #             df.to_csv('CommentsOnly.csv.csv')
    #     print('ID为{}的微博评论爬取完毕'.format(ID))
    def run(self):

        num_page = 30
        with open('./input file/wbURL', 'r') as f:
            urls = f.readlines()
            for i in range(len(urls)):  # len得到list长度，range表示从0到len长度的区间
                try:
                    wb_url = urls[i]
                    print(wb_url)
                    return_info = ('0', '0')
                    for i in range(0, num_page):
                        print(f'正在爬取第{i + 1}页')
                        time.sleep(20)
                        self.params = {
                            'id': wb_url,
                            'mid': wb_url,
                            'max_id': return_info[0],
                            'max_id_type': return_info[1]
                        }
                        return_info = self.get_max_id()
                    data = []
                    for text in self.list_text:
                       data.append([i, text])

                        # s = ('第{}条微博数据爬取完毕'.format(i))
                        # print('ID为{}的微博评论爬取完毕'.format(wb_url))
                    print('第{}条微博,ID为{},评论爬取完毕'.format(i,wb_url))

                except:
                    print('第{}条微博评论爬取失败'.format(i))
                    # df = pd.DataFrame(data, columns=['wb_url', 'comment'])
                    # # df = df.append(wb_url)
                    # df.to_csv('./outputs/lastcomment.csv')
                # for text in self.list_text:
                df = pd.DataFrame(data, columns=['wb_url', 'comment'])
                # df = df.append(wb_url)
                df.to_csv('./outputs/lastcomment.csv')




        # self.save_data()
    # with open('./input file/wbURL', 'r') as f:
    #     wb_url = f.readlines()
    # def save_data(self):
    #     data=[]
    #     for text in self.list_text:
    #         data.append([wb_url, text])
    #         df = pd.DataFrame(data, columns=['url', 'comment'])
    #         df.to_csv('CommentsOnly.csv.csv')
            # with open('weibo.txt', 'a', encoding='utf-8') as f:
            #     f.write(text)
            #     f.write('')
            #     f.write('\n')

if __name__ == '__main__':
    getComments = WBcomments()
    getComments.run()
    # with open('./input file/wbURL', 'r') as f:
    #     urls = f.readlines()
    #     for i in range(len(urls)):  # len得到list长度，range表示从0到len长度的区间
    #         try:
    #             wb_url = urls[i]
    #             print(wb_url)
    #             getComments.run(wb_url)
    #             print('第{}条微博评论爬取完毕'.format(i))
    #         except:
    #             print('第{}条微博评论爬取失败'.format(i))

