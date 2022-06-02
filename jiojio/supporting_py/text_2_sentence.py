# -*- coding=utf-8 -*-

import os
import pdb
import json
import jionlp as jio


tokens = ['。', '！', '？', ]
datasets = list()
file_path = '/home/cuichengyu/dataset/cws/cws.txt'
# file_path = '/home/cuichengyu/dataset/bosson/all_tuned_pos.json'
stop_char_num = 0

with open('/home/cuichengyu/dataset/cws/sentences.txt', 'w', encoding='utf-8') as fw:
    for idx, line in enumerate(jio.read_file_by_iter(file_path)):
        text = line
        # tags = line[1]
        if len(text) < 30:
            # datasets.append(line)
            if '。' in text[:-1]:
                stop_char_num += 1
            if '！' in text[:-1]:
                stop_char_num += 1
            if '？' in text[:-1]:
                stop_char_num += 1
            fw.write(json.dumps(line, ensure_ascii=False) + '\n')
            continue

        datasets = list()
        # print(line)
        offset = 0
        for i in range(len(text)):
            if text[i] in tokens:
                tmp = text[offset: i+1]
                if len(tmp) == 1:
                    # print(line)
                    if len(datasets) == 0:
                        pass
                    else:
                        datasets[-1].extend(tmp)
                        # datasets[-1][1].extend(tags[offset: i+1])
                    # pdb.set_trace()
                    # print(datasets[-1])
                else:
                    datasets.append(text[offset: i+1])
                offset = i + 1
                # pdb.set_trace()
        # print(line[offset:])
        if offset < len(text):
            datasets.append(text[offset:])
        # pdb.set_trace()

        if idx % 100000 == 0:
            print(idx, len(datasets), stop_char_num)

        for item in datasets:
            # assert len(item[0]) == len(item[1])
            # print('  '.join([c + '/' + t for c, t in zip(item[0], item[1])]))
            fw.write(json.dumps(item, ensure_ascii=False) + '\n')

print('stop char num: ', stop_char_num)

# import random
# random.shuffle(datasets)
# jio.write_file_by_line(datasets, '/home/cuichengyu/dataset/cws/sentences.txt')
