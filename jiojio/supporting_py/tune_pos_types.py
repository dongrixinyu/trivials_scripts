# -*- coding=utf-8 -*-

import os
import pdb
import sys
import json
import random
import collections
import numpy as np
from jiojio import read_file_by_iter, write_file_by_line


bosson_dir = '/home/cuichengyu/dataset/bosson'

bosson_map_dict = {
    # 'w': 'wx',  # 所有非常规标点映射为其它标点类型 ① 映射为数词
    'wb': 'w', 'wd': 'w', 'wf': 'w', 'wj': 'w', 'wm': 'w', 'wn': 'w',
    'ws': 'w', 'wt': 'w', 'ww': 'w', 'wky': 'w', 'wkz': 'w', 'wyy': 'w', 'wyz': 'w',
    'wp': 'w',  # 所有常规标点映射为同一个类型 w
    'wh': 'q',  # 单位符号 $ 映射为单位词
    # 'wb': 'm',  # 百分号千分号应当为数词的一部分，除非单独出现
    'pba': 'p', 'pbei': 'p',  # 介词进行类型统一
    'ude': 'u', 'udeng': 'u', 'udh': 'u', 'uguo': 'u', 'ulian': 'u', 'usuo': 'u',
    'uyy': 'u', 'uzhe': 'u', 'uzhi': 'u',  # 所有助词统一化 u
    'email': 'x', 'id': 'x', 'url': 'x', 'ip': 'x',

    'vshi': 'v', 'vyou': 'v',  # 将两种特殊动词合并为一种动词
    'y': 'u',  # 语气助词也属于助词的一种。
    'b': 'a', 'bl': 'al', 'z': 'a',  # 区别词、状态词直接归入形容词
    'nx': 'x',  # 非中文的字符串，全部转为 x 类型，原因是 nx 很大程度不具有名词属性，
                # 但是一些英文符号具有专有名词特性

}

file_name = 'all_pos.json'

all_sample_list = list()
all_tag_list = list()
num = '0123456789１２３４５６７８９０'
special_num = '①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛㈠㈡㈢㈣㈤㈥㈦㈧㈨㈩'
percentage = '％%‰'
for line_idx, line in enumerate(read_file_by_iter(os.path.join(bosson_dir, file_name))):
    words_list = line[0]
    tags_list = line[1]

    new_words_list = list()
    new_tags_list = list()
    for idx, (word, tag) in enumerate(zip(words_list, tags_list)):
        if tag == 'wb':
            if word in percentage:
                if idx - 1 >= 0 and words_list[idx - 1][-1] in num:  # 把百分号和之前的数字合在一起
                    new_tags_list[-1] = 'm'
                    new_words_list[-1] = new_words_list[-1] + word
                    # print(new_words_list[-3:])
                    # print(new_tags_list[-3:])
                    # pdb.set_trace()
                    continue
                else:
                    new_tags_list.append('wx')
                    new_words_list.append(word)
                    continue
            else:
                # print('wb', 'wx', word)
                # pdb.set_trace()
                new_tags_list.append('wx')
                new_words_list.append(word)
                continue
        elif tag == 'k':  # 后缀，和 前一个相结合
            try:
                if word == '型':
                    before_tag = tags_list[idx - 1]
                    if before_tag in ['nx', 'm', 'nrf']:
                        new_tags_list[-1] = 'nz'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['n', 'r', 'ns', 'q']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['a', 'b', 'd', 'bl']:
                        new_tags_list[-1] = 'an'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['v', 'vi', 'vl']:
                        new_tags_list[-1] = 'an'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'p', 'c', 'u']:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'an'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                elif word == '观':
                    before_tag = tags_list[idx - 1]
                    if before_tag in ['n']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['ns']:
                        new_tags_list[-1] = 'ns'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    else:
                        new_tags_list.append('vn')
                        new_words_list.append(word)
                        continue
                elif word == '们':
                    before_tag = tags_list[idx - 1]
                    if before_tag in ['n', 'nr', 'nrf', 'nx', 'nl', 'r', 'k']:
                        new_tags_list[-1] = before_tag
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['vi', 'ns', 'v', 'f', 'z', 'k', 'b', 'a', 'ad']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'p', 'd', 'c', 'u']:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word == '式':
                    before_tag = tags_list[idx - 1]
                    if before_tag in ['n', 's', 'v', 'z', 'vi', 'ad', 'm', 'd', 'b', 'ns', 't', 'a', 't', 'q']:
                        new_tags_list[-1] = 'an'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['nl', 'vl', 'al', 'bl', 'dl']:
                        new_tags_list[-1] = 'al'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['nx', 'nrf', 'nr', 'nz']:
                        new_tags_list[-1] = 'nz'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p']:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'an'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                elif word == '性':
                    before_tag = tags_list[idx - 1]
                    if '率性' in new_words_list[-1] + word:
                        new_tags_list[-1] = 'a'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                    if before_tag in ['n', 'm', 'f','v', 'vl', 'vi', 'a', 'b', 'nx', 'ad', 'z', 'nz']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                    elif before_tag in ['d', 't']:
                        new_tags_list[-1] = 'a'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'u', 'p', 'r', 'nrf', ]:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                elif word == '制':
                    before_tag = tags_list[idx - 1]
                    if new_words_list[-1] + word in ['熏制', '入制', '兼制']:
                        new_tags_list[-1] = 'v'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                    if before_tag in ['n', 'v', 'vi', 'a', 'ns', 'nr', 'nl', 'nx']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p', 'r', 'nrf', ]:
                        new_tags_list.append('v')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word == '业':
                    before_tag = tags_list[idx - 1]
                    if before_tag in ['n', 'v', 'vi', 'ns', 'nr', 'nl', 'nx']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p', 'r', 'nrf', ]:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word == '者':
                    before_tag = tags_list[idx - 1]
                    if new_words_list[-1] + word in ['行者']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                    if before_tag in ['n', 'v', 'f', 'q', 'z', 'vi', 'ns', 'a', 'nr', 'r', 'nx', 'nrf', 'vd']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    if before_tag in ['nl', 'vl']:
                        new_tags_list[-1] = 'nl'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p', 'u']:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word == '化':
                    before_tag = tags_list[idx - 1]
                    if '年化' in new_words_list[-1] + word:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                    if before_tag in ['n', 'd', 'z', 'v', 'nz', 'b', 'a', 'vi', 'ns', 'nr', 'r', 'nl', 'nx', 'nrf']:
                        new_tags_list[-1] = 'an'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p']:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'an'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word == '度':
                    before_tag = tags_list[idx - 1]

                    if before_tag in ['n', 'a', 'b', 'd', 'v', 'vi', 'ns', 'nr', 'r', 'nl', 'nx', 'nrf']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p']:
                        new_tags_list.append('v')
                        new_words_list.append(word)
                        continue
                    elif before_tag in ['t']:
                        new_tags_list[-1] = 't'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                elif word == '率':
                    before_tag = tags_list[idx - 1]

                    if before_tag in ['n', 'a', 'v', 'vi', 'ns', 'nr', 'r', 'nl', 'nx', 'nrf', 'k']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p', 'u']:
                        new_tags_list.append('v')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word == '法':
                    before_tag = tags_list[idx - 1]

                    if before_tag in ['n', 'a', 'd', 'v', 'vi', 'ns', 'nr', 'r', 'nl', 'nx', 'nrf']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p', 'u']:
                        new_tags_list.append('v')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word == '儿':
                    before_tag = tags_list[idx - 1]

                    if before_tag in ['n', 'v', 'b', 'q', 'vi', 'ns', 'r', 'nl', 'nx', 'nrf']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['nr']:
                        new_tags_list[-1] = 'nr'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p']:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue

                elif word in ['感', '论']:
                    before_tag = tags_list[idx - 1]

                    if before_tag in ['n', 'an', 'v', 't', 'a', 'vi', 'ns', 'r', 'nl', 'nx', 'nrf']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p', 'u']:
                        new_tags_list.append('v')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                elif word == '乎':
                    new_tags_list[-1] = 'nz'
                    new_words_list[-1] = new_words_list[-1] + word
                    continue
                elif word == '边':
                    before_tag = tags_list[idx - 1]
                    if before_tag in ['w']:
                        new_tags_list.append('p')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                elif word in ['类', '界', '家', '头', '症', '仪', '版', '体', '长',
                        '堆', '热', '单']:
                    before_tag = tags_list[idx - 1]

                    if before_tag in ['n', 'a', 'b', 'ad', 'v', 'vi', 'ns', 'r', 'nl', 'nx', 'nrf']:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
                    elif before_tag in ['w', 'wx', 'c', 'p']:
                        new_tags_list.append('n')
                        new_words_list.append(word)
                        continue
                    else:
                        new_tags_list[-1] = 'n'
                        new_words_list[-1] = new_words_list[-1] + word
                        continue
            except:
                continue

        # elif tag == 'w':
        #     if word in special_num:
        #         new_tags_list.append('m')
        #         new_words_list.append(word)
        #         continue
        #     else:
        #         new_tags_list.append('wx')
        #         new_words_list.append(word)
        #         continue


        else:
            before_tag = tags_list[idx - 1]
            before_word = words_list[idx - 1]
            if before_tag == 'h':
                try:
                    if before_word == '非':

                        if tag in ['nx', 'n', 'nrf', 'nz', 'nl', 'nr', 'ns', 'r', 't', 's', 'f']:
                            new_tags_list[-1] = 'a'
                            new_tags_list.append(bosson_map_dict.get(tag, tag))
                            new_words_list.append(word)
                            # pdb.set_trace()
                            continue

                        elif before_tag in ['d', 'vd', 'vi', 'vl', 'v', 'ad', 'a', 'b', 'z']:
                            new_tags_list[-1] = 'd'
                            new_tags_list.append(bosson_map_dict.get(tag, tag))
                            new_words_list.append(word)
                            continue
                        else:
                            new_tags_list[-1] = 'a'
                            new_tags_list.append(bosson_map_dict.get(tag, tag))
                            new_words_list.append(word)
                            continue

                    elif before_word == '亚':
                        if before_word + word in ['亚硝酸钠', '亚健康', '亚太股市', '亚特兰蒂斯', '亚麻',
                                '亚开行']:
                            new_tags_list[-1] = 'n'
                            new_words_list[-1] = before_word + word
                            continue

                        new_tags_list[-1] = 'a'
                        new_tags_list.append(bosson_map_dict.get(tag, tag))
                        new_words_list.append(word)
                        continue
                    elif before_word in ['准', '预', '超', '微', '泛']:
                        new_tags_list[-1] = 'a'
                        new_tags_list.append(bosson_map_dict.get(tag, tag))
                        new_words_list.append(word)
                        continue
                    else:
                        new_words_list[-1] = before_word + word
                        continue
                except:
                    continue
            else:
                new_tags_list.append(bosson_map_dict.get(tag, tag))
                new_words_list.append(word)
                continue

    if len(new_tags_list) != len(new_words_list):
        print(new_words_list)
        print(new_tags_list)
        continue
        pdb.set_trace()

    all_tag_list.extend(new_tags_list)
    all_sample_list.append([new_words_list, new_tags_list])
    if line_idx % 100000 == 0:
        print(line_idx)


freq_counter = collections.Counter()
freq_counter.update(all_tag_list)
for item, freq in freq_counter.most_common():
    print(item, '\t', '{:.3%}'.format(freq / len(all_tag_list)), '\t', freq)
print('all_tuned pos tag: ', len(list(set(all_tag_list))), list(set(all_tag_list)))

with open(os.path.join(bosson_dir, 'all_tuned_pos.json'), 'w', encoding='utf-8') as fw:
    for item in all_sample_list:
        fw.write(json.dumps(item, ensure_ascii=False) + '\n')
