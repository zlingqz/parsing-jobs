# 核心步骤：
# fre = jieba.analyse.textrank(texts,topK=400,withWeight=True) #保留最高频的400个词
# cloud = WordCloud(......)
# wc = cloud.generate_from_frequencies(fre) #产生词云
# wc.to_file("weibo_cloud.jpg") #保存图片


import re
import jieba
from scipy.misc import imread
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
import matplotlib.pyplot as plt
from os import path
import jieba.analyse

f = open('han.txt')
tweets = f.readlines()
f.close()

zhongwen_pat = re.compile(r'^[\u4e00-\u9fa5a-zA-Z]+$')
all_content = []
f = open("rmw.txt","w")
for t in tweets: #tweets是从数据库中取出来的待制作词云图的文本源
    cut_list = [c for c in jieba.cut(t[0]) if zhongwen_pat.search(c)]
    cut_set = set(cut_list)
    # res_set = cut_set - stopdict
    res_set = cut_set
    res_list = list(res_set)
    all_content.extend(res_list)
    f.writelines(res_list)
f.close()

def get_top_keywords(file): #这里的file即上一步生成的“weibo.txt”
    top_word_dict = {} # 关键词列表，待填充
    with open(file,'r') as f:
        texts = f.read() # 读取整个文件作为一个字符串
        result = jieba.analyse.textrank(texts,topK=400,withWeight=True) #保留最高频的400个词
        for r in result:
            top_word_dict[r[0]] = r[1]
    return top_word_dict


def draw_wordcloud(txt):
    #读入一个txt文件,基于此文本知错词云图
    d = path.dirname(__file__) #当前文件文件夹所在目录
    print(d)
    color_mask = imread("yu.jpg") #读取背景图片，
    cloud = WordCloud(
        #设置字体，不指定就会出现乱码，文件名不支持中文
        font_path="msyh.ttc",
        #font_path=path.join(d,'simsun.ttc'),
        #设置背景色，默认为黑，可根据需要自定义为颜色
        background_color='black',
        #词云形状，
        mask=color_mask,
        #允许最大词汇
        max_words=400,
        #最大号字体，如果不指定则为图像高度
        max_font_size=100,
        #画布宽度和高度，如果设置了msak则不会生效
        width=600,
        height = 400,
        margin = 2,
        #词语水平摆放的频率，默认为0.9.即竖直摆放的频率为0.1
        prefer_horizontal = 0.8
    )
    wc = cloud.generate_from_frequencies(txt) #产生词云
    #wc = cloud.fit_words(txt) 跟以上是同一意思
    wc.to_file("weibo_cloud.jpg") #保存图片
    # #显示词云图片
    # plt.imshow(wc)
    # #不现实坐标轴
    # plt.axis('off')
    # #绘制词云
    # #plt.figure(dpi = 600)
    # image_colors = ImageColorGenerator(color_mask)
    # #plt.imshow(wc.recolor(color_func=image_colors)) 重新上色，
    # plt.show()

if __name__ == "__main__":
    fre = get_top_keywords("han.txt")
    draw_wordcloud(fre)
    # # 将频率输出到文本，可以修改文本的内容重新画图
    # f = open("top400.txt", "w")
    # for key, value in fre.items():
    #     a = key + "\t" + str(value) + "\n"
    #     f.write(a)
    # f.close()
    # fre = dict()
    # f = open("top400.txt", "r")
    # for line in f.readlines():
    #     line.strip()
    #     t = line.split('\t')
    #     fre[t[0]] = float(t[1])
    # f.close()
    # draw_wordcloud(fre)

