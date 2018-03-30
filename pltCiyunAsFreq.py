# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name:   pltCiyunAsFreq
   Description: 
   Author:      LOVE
   Date:        2018/3/30 20:17
-------------------------------------------------
   Change Activity:
                2018/3/30: 
-------------------------------------------------
"""
__author__ = 'LOVE'

from config import *
from wordcloud import WordCloud
import codecs
import jieba
import jieba.analyse as analyse
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

    # Extract keywords from sentence using TextRank algorithm, 仅包含名词
    textRank = analyse.textrank(input_text, topK=200, withWeight=True, allowPOS=('ns', 'n'))
    print("Extract keywords from sentence using TextRank algorithm:")

    with open('CNRank.txt', 'w', encoding="utf-8") as f:
        for tr in textRank:
            print(tr)
            f.write(tr[0] + '\t:\t' + str(tr[1]) + '\n')

    # Extract keywords from sentence using TF-IDF algorithm, 仅包含名词
    tfidf = analyse.extract_tags(input_text, topK=200, withWeight=True, allowPOS=('ns', 'n'))
    print("Extract keywords from sentence using TF-IDF algorithm:")
    for tf in tfidf: print(tf)

    # 精确模式，输出前200最高词频的文本
    tags = jieba.cut(input_text)
    most = Counter(tags).most_common(200)
    print("默认为精确模式，试图将句子最精确地切开，适用于文本分析，cut_all=False, HMM=True:")
    for w in most: print(w)

    # jieba分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    # tags = jieba.cut(input_text)
    # cut_text = " ".join(tags)

    d = path.dirname(__file__)  # 当前文件文件夹所在目录
    color_mask = imread("Trump.png")  # 读取背景图片
    cloud = WordCloud(
        font_path="heiti.ttf",  # 设置字体，不指定就会出现乱码，须单独下载到运行目录
        # width=4000,   # 长
        # height=3000,  # 宽
        background_color='white',  # 设置背景色
        prefer_horizontal=1,    # 水平比例
        mask=color_mask,  # 词云形状
        max_words=200,  # 允许最大词汇
        # min_font_size=10, # 最小字号
        max_font_size=200,  # 最大字号
        random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
    )
    keywords = dict(textRank)
    word_cloud = cloud.generate_from_frequencies(keywords)  # 使用关键字词频产生词云
    word_cloud.to_file("cq_DA_CN_Freq.jpg")  # 保存图片
    #  显示词云图片
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()


if __name__ == '__main__':
    draw_wordcloud()
