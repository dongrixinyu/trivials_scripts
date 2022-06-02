# -*- coding=utf-8 -*-

import os
import pdb
import sys
import json
import numpy as np
from jiojio import read_file_by_iter, write_file_by_line


bosson_dir = '/home/cuichengyu/dataset/bosson'


# bosson_tags_dict = dict([(tag, list()) for tag in bosson_tags])
all_tags = list()
bosson_file_list = os.listdir(bosson_dir)

all_k = dict()

for idx, line in enumerate(read_file_by_iter(
        os.path.join(bosson_dir, 'all_pos.json'))):#, line_num=10000)):
    # all_tags.extend(line['tag'])

    for idx_p, (word, tag) in enumerate(zip(line[0], line[1])):
        if np.random.random() < 0.1:
            if tag == 'h':
                # start = max(0, idx_p - 4)
                # end = idx_p + 4
                # res = [word + '/' + tag for word, tag in zip(
                #     line[0][start: end], line[1][start: end])]
                # print('   '.join(res))
                try:
                    if word not in all_k:
                        all_k.update(
                            {word: [1, [''.join(line[0][idx_p: idx_p + 2]) + '/' + line[1][idx_p + 1]]]})
                    else:
                        all_k[word][0] += 1
                        all_k[word][1].append(''.join(line[0][idx_p: idx_p + 2]) + '/' + line[1][idx_p + 1])
                    # pdb.set_trace()
                except:
                    continue
    if idx % 100000 == 0:
        print(idx)

for k in all_k:
    all_k[k][1] = list(set(all_k[k][1]))
pdb.set_trace()

with open('pos_h.json', 'w', encoding='utf-8') as fw:
    json.dump(all_k, fw, ensure_ascii=False, indent=4, separators=(',', ':'))
print(all_k.keys())
