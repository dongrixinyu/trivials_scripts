# -*- coding=utf-8 -*-

import os
import pdb
import sys
import json
import random
import numpy as np
from jiojio import read_file_by_iter, write_file_by_line


bosson_dir = '/home/cuichengyu/dataset/bosson'

bosson_tags = ['q', 'wky', 'vn', 'uzhe', 'nl', 'p', 'vd', 'vi', 'v', 't', 'y', 's', 'r',
               'wp', 'ulian', 'url', 'wh', 'al', 'n', 'wj', 'ns', 'usuo', 'wyz', 'm', 'nt',
               'd', 'z', 'id', 'wf', 'wd', 'dl', 'nr1', 'nrf', 'uyy', 'ip', 'u', 'bl', 'ad',
               'nx', 'o', 'h', 'wyy', 'w', 'pbei', 'wn', 'ww', 'udeng', 'ude', 'vshi', 'k',
               'ws', 'f', 'vl', 'wb', 'an', 'nr', 'wt', 'wkz', 'vyou', 'uzhi', 'uguo',
               'udh', 'c', 'a', 'b', 'email', 'wm', 'nz', 'pba']
all_tags = ['a', 'nd', 'k', 'u', 'h', 'd', 'v', 'nhf', 'r', 'j', 'nt', 'x', 'nl',
            'o', 'q', '01', 'w', 'n', 'vu', 'vd', 'ni', 'i', 'm', 'nz', 'f', 'ns',
            'e', 'c', 'nh', 'ws', 'p', 'vl', 'nhs', 'g', 'mq']


bosson_tags_dict = {
    'a': '形容词',  # 恬静，博，浑，不均，可信，匀称，美观
    'ad': '副形词',  # 正常，科学，真诚，主动，独立，及时
    'al': '形容词惯用语',  # 跌宕起伏，可圈可点，坚韧不拔，理所当然
    'an': '名形词',  # 麻烦，冲动，骄傲，民主，平衡
    'b': '区别词',  # 助力，自动，广大，特有，优质，隐形
    'bl': '区别词惯用语',  # 五花八门，廉洁自律，总的来说，无独有偶，光天化日
    'c': '连词',  # 可见，紧接着，既，以免，要不是，从而，另一方面，与此同时
    'd': '副词',  # 略微，颇，不免，即刻，原，不禁
    'dl': '副词惯用语',  # 接下来，自始至终，为时已晚，整体而言，说到底
    'email': 'email',  # fengbaodan@126.com
    'f': '方位词',  # 初，期间，同期，顶部，侧向，中期，顶层，身后，零下
    'h': '前缀词',  # 超，非，亚，准
    'id': '身份证号',  # 873518471269518471，61012519910311667X
    'ip': 'ip',  # 009.271.441.350，1.705.665.70
    'k': '后缀词',  # 化，感，制，性，度，业，式，法，们，类，者，型，率
    'm': '数词',  # 78，281.1万，4.08%01109，3.58%，第一百九十三，54，大半
    'n': '名词',  # 外籍，出版物，滑雪场，残留量，风致
    'nl': '名词性惯用语',  # 兵家必争之地，社会保险，经济基础，责任事故
    'nr': '人名',  # 曹静静，半夏，赵松，苏某芹，热某，江某某
    'nr1': '中文姓氏',  # 汪，希，丁，曹，许，冯
    'nrf': '外文名',  # 斯普拉克伦，科什拉科夫，本·阿里，卡罗琳·皮尔
    'ns': '地名',  # 荆州市，大湾区，西班牙，石狮，武威，肇庆市
    'nt': '组织机构名',  # 热刺队，▷眼部，救援队，八局，政法委
    'nx': '字符串',  # Muslim，team-mate，pela，Many，collection
    'nz': '专有名词',  # 成集永锋，英特尔，森凌，安诚山，可口可乐，电通，骁龙
    'o': '拟声词',  # 丁，砰，哈哈，滴滴，扑通，咚咚
    'p': '介词',  # 基于，随，处以，靠，关于，离，沿着，用
    'pba': '把',  # 介词
    'pbei': '被',  # 介词
    'q': '量词',  # 次、架、澳元、层、斤
    'r': '代词',  # 我委，另，各校，每瓶，各项，该片，本场，该厂
    's': '处所词',  # 场内，零下，现场，空中，前沿，海边，心中，地上
    't': '时间词',  # 现，便后，今晨，午夜，14:51:19
    'url': 'url',  # 1.jp，http://m.weibo.cn/2703294971/44101
    'u': '助词',  # 来说，来讲，而言，案，一般
    'ude': '的地得',  # 助词
    'udeng': '等',  # 助词
    'udh': '的话',  # 助词
    'uguo': '过',  # 助词
    'ulian': '连',  # 助词
    'usuo': '所',  # 助词
    'uyy': '一样',  # 助词
    'uzhe': '着',  # 助词
    'uzhi': '之',  # 助词
    'v': '动词',  # 告，任命，切断，搅拌，确保，入主，接管
    'vd': '副动词',  # 照常，综合，自主，密闭，统筹，批量化，辅助，免费
    'vi': '不及物动词',  # 投稿，辞职，还债，兜，保值，不已，发财
    'vl': '动词性惯用语',  # 开诚布公，一笔勾销，不言而喻，夸大其词，销声匿迹
    'vn': '名动词',  # 清零，发布，涉案，套现，上传，热议
    'vshi': '是',  # 是，就是，动词
    'vyou': '有',  # 动词
    'w': '标点符号',  # 丨☛+①┃==============＋&▽
    'wb': '百分号',  # ％，%
    'wd': '逗号',  # ,，
    'wf': '分号',  # ；，;
    'wh': '单位符号',  # ￥＄￡°℃$
    'wj': '句号',  # .。．
    'wm': '冒号',  # :：
    'wn': '顿号',  # 、
    'ws': '省略号',  # ……
    'wt': '叹号',  # !！
    'ww': '问号',  # ?？
    'wky': '括号右半部',  # >>>)〕】
    'wyy': '引号右半部',  # ’』”」
    'wkz': '扩号左半部',  # 〔<（（（《
    'wyz': '引号左半部',  # "，“，『，‘，「
    'wp': '破折号',  # ---，--，——，－，————，——————
    'y': '语气词',  # 吗，也，喔，呢，而已，啦
    'z': '状态词',  # 随机，各异，持刀，沉甸甸，蔓蔓，长长的，漫漫
}

bosson_map_dict = {
    'w': 'wx',  # 所有非常规标点映射为其它标点类型 ① 映射为数词
    'wb': 'w', 'wd': 'w', 'wf': 'w', 'wj': 'w', 'wm': 'w', 'wn': 'w',
    'ws': 'w', 'wt': 'w', 'ww': 'w', 'wky': 'w', 'wkz': 'w', 'wyy': 'w', 'wyz': 'w',
    'wp': 'w',  # 所有常规标点映射为同一个类型 w
    'wh': 'q',  # 单位符号 % 映射为单位词
    'wb': 'm',  # 百分号千分号应当为数词的一部分，除非单独出现
    'pba': 'p', 'pbei': 'p',  # 介词进行类型统一
    'ude': 'u', 'udeng': 'u', 'udh': 'u', 'uguo': 'u', 'ulian': 'u', 'usuo': 'u',
    'uyy': 'u', 'uzhe': 'u', 'uzhi': 'u',  # 所有助词统一化 u
    'email': 'x', 'id': 'x', 'url': 'x',
    'y': 'u',  # 语气助词，依然为助词的一种。由于数量不多，应当合并
    'nx': 'x',  # 非中文的字符串，全部转为 x 类型，原因是 nx 很大程度不具有名词属性
}


bosson_tags_dict = dict([(tag, list()) for tag in bosson_tags])
all_tags = list()
bosson_file_list = os.listdir(bosson_dir)
for file_name in bosson_file_list:
    if 'all_text' in file_name:
        for idx, line in enumerate(read_file_by_iter(os.path.join(bosson_dir, file_name), line_num=100)):
            # all_tags.extend(line['tag'])
            for word, tag in zip(line['word'], line['tag']):
                if np.random.random() < 0.0001:
                    bosson_tags_dict[tag].append(word)
            if idx % 100000 == 0:
                print(idx)

for tag in bosson_tags:
    bosson_tags_dict[tag] = list(set(bosson_tags_dict[tag]))
    random.shuffle(bosson_tags_dict[tag])

# pdb.set_trace()
# all_tags = list(set(all_tags))
# print(all_tags)

'''
with open('pos_tags_description.txt', 'w', encoding='utf-8') as fw:
    for tag in bosson_tags:
        line = tag + '\t' + '，'.join(bosson_tags_dict[tag][:100]) + '\n'
        fw.write(line)
'''

# sys.exit()

orig_file = '/home/cuichengyu/dataset/pos_all.json'

dataset = list()
all_tags = ['a', 'nd', 'k', 'u', 'h', 'd', 'v', 'nhf', 'r', 'j', 'nt', 'x', 'nl',
            'o', 'q', '01', 'w', 'n', 'vu', 'vd', 'ni', 'i', 'm', 'nz', 'f', 'ns',
            'e', 'c', 'nh', 'ws', 'p', 'vl', 'nhs', 'g', 'mq']
# all_tags = list()
tags_dict = dict([(tag, list()) for tag in all_tags])
for idx, line in enumerate(read_file_by_iter(orig_file)):
    # 出场/v ，/w 用尽/v 一切/r 手段/n 死死/d 缠住/v 天津/ns 队员/n ，/w 阻止/v 进攻/v ，/w 拖延/v 时间/n 以/p 保住/v ０/m ./w ５/m 的/u 优势/n 。/w
    for word, tag in zip(line[0], line[1]):
        if np.random.random() < 0.01:
            tags_dict[tag].append(word)
            # pass
        # all_tags.append(tag)
        # pdb.set_trace()

    if idx % 100000 == 0:
        print(idx)

# print(list(set(all_tags)))
for tag in all_tags:
    tags_dict[tag] = list(set(tags_dict[tag]))
    random.shuffle(tags_dict[tag])

with open('pos_tags_description1.txt', 'w', encoding='utf-8') as fw:
    for tag in all_tags:
        line = tag + '\t' + '，'.join(tags_dict[tag][:100]) + '\n'
        fw.write(line)
