# -*- coding=utf-8 -*-

import os
import re
import pdb
from collections import Counter

import jionlp as jio


dir_path = '/home/cyy/datasets/cws'
file_name = 'sentences_{}.txt'

# ptn = re.compile(r'(((.).\3.)|((.)\5(.)\6))')


AABB_list = ['拼多多', '聚美优品', '唯品会', '苏宁易购', '宁德时代', '比亚迪', '药明康德']
ptn = re.compile(r'(' + '|'.join(AABB_list) + ')')
dc_with_standard_words = jio.cws.CWSDCWithStandardWords(AABB_list)

pdb.set_trace()
AABB_counter = Counter()
for i in range(4):
    file_path = os.path.join(dir_path, file_name.format(i))
    print(file_path)
    new_list = list()
    replace_num = 0
    for idx, line in enumerate(jio.read_file_by_iter(file_path)):
        text = ''.join(line)

        res = ptn.search(text)
        if res is not None:
            word = res.group()
            # start from here!!!!!!!!!!!!!!!!!!!!!!!!!!
            if word not in line and word in AABB_list:  # and (word[:2] not in line or word[2:] not in line):
                # print(res)
                # print(' '.join(line))
                corrected = dc_with_standard_words(line, verbose=False)
                # print(' '.join(corrected))
                replace_num += 1
                new_list.append(corrected)

                # pdb.set_trace()
                continue

        new_list.append(line)
        #         AABB_counter.update([word])
# AABB_list = [[item[0], item[1]] for item in AABB_counter.most_common()[:460]]
# pdb.set_trace()
    print('repalced {} AABB words'.format(replace_num))
    print('sample_num: {}'.format(len(new_list)))
    # pdb.set_trace()
    jio.write_file_by_line(new_list, os.path.join(dir_path, file_name.format(i)+ '.correct'))


print('finished!')
