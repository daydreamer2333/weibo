import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt  # 绘制图像的模块
import jieba.analyse as anls  # 关键词提取
import re
from collections import Counter

'''功能描述：
   1、读取文本
   2、分词
   3、加载停用词表
   4、去停用词
   5、提取关键词2种方法
   6、画词云展示
'''

# 1、读取文本
text = open("outputs/wordcloud.txt", 'r', encoding='utf-8').read()
# 加载停用词表
stopwords = [line.strip() for line in open('./dictionary/Chinese_stop_words.txt', encoding='UTF-8').readlines()]  # list类型
# 分词未去停用词
text_split = jieba.cut(text)  # 未去掉停用词的分词结果   list类型

# 去掉停用词的分词结果  list类型
text_split_no = []
for word in text_split:
    if word not in stopwords:
        text_split_no.append(word)
# print(text_split_no)

text_split_no_str = ' '.join(text_split_no)  # list类型分为str

# 基于tf-idf提取关键词
print("基于TF-IDF提取关键词结果：")
keywords = []
for x, w in anls.extract_tags(text_split_no_str, topK=300, withWeight=True):
    keywords.append(x)  # 前20关键词组成的list
keywords = ' '.join(keywords)  # 转为str
print(keywords)

# 画词云
wordcloud = WordCloud(
    # 设置字体，不然会出现口字乱码，文字的路径是电脑的字体一般路径，可以换成别的
    font_path="C:/Windows/Fonts/simkai.ttf",
    # 设置了背景，宽高
    background_color="white", width=1000, height=880).generate(keywords)  # keywords为字符串类型

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

