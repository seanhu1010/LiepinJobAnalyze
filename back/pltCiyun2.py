# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   pltCiyun2
   Description: 
   Author:      LOVE
   Date:        2018/3/28 22:32
-------------------------------------------------
   Change Activity:
                2018/3/28: 
-------------------------------------------------
"""
from config import *
from wordcloud import WordCloud
import codecs
import jieba
# import jieba.analyse as analyse
from scipy.misc import imread
import os
from os import path
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
from collections import Counter

# 绘制词云
def draw_wordcloud():
    # 读入一个txt文件
    input_text = open(MONGO_TABLE + ".txt", 'rb').read()

    # jieba分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    # 默认为精确模式，试图将句子最精确地切开，适用于文本分析，cut_all=False, HMM=True
    tags = jieba.cut(input_text)

    # 输出前100最高词频的文本
    # most = Counter(tags).most_common(100)
    # for w in most: print(w)

    cut_text = " ".join(tags)


    d = path.dirname(__file__)  # 当前文件文件夹所在目录
    color_mask = imread("Trump.png")  # 读取背景图片
    cloud = WordCloud(
        font_path="heiti.ttf",  # 设置字体，不指定就会出现乱码
        # font_path=path.join(d,'simsun.ttc'),
        #width=4000,
        #height=3000,
        background_color='white',  # 设置背景色
        prefer_horizontal = 1,
        mask=color_mask,  # 词云形状
        max_words=400,  # 允许最大词汇
        #min_font_size=10,
        max_font_size=200,  # 最大号字体
        random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
    )
    word_cloud = cloud.generate(cut_text)  # 产生词云
    word_cloud.to_file("pjl_cloud1.jpg")  # 保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    draw_wordcloud()
