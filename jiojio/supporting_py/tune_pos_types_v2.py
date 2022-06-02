# -*- coding=utf-8 -*-
# 在原先调整过的词性基础上，再合并几种类型，即把 l 俗语类型去掉，按其词性进行划分。
# 例如：美轮美奂，应当是形容词，至于是否是俗语成语，则不重要。
# vn 名动词，本质上是一种非谓语动词，但是为了应对短语抽取等情况，直接将其归为动词。

import os
import pdb
import json
import jionlp as jio


dir_name = '/home/cuichengyu/dataset/bosson'
file_name = 'sentences.txt'
tuned_file_name = 'tuned_sentences.txt'

map_dict = {'vn': 'v', 'nl': 'n',
            'vl': 'v', 'al': 'a', 'dl': 'd'}

with open(os.path.join(dir_name, tuned_file_name), 'w', encoding='utf-8') as fw:
    for idx, line in enumerate(jio.read_file_by_iter(os.path.join(dir_name, file_name))):
        # print(line)
        new_line = list()
        new_line.append(line[0])
        new_tags = list()
        for tag in line[1]:
            if tag in map_dict:
                new_tags.append(map_dict[tag])
            else:
                new_tags.append(tag)
        new_line.append(new_tags)
        # print(new_line)

        fw.write(json.dumps(new_line, ensure_ascii=False) + '\n')
        # pdb.set_trace()
