# -*- coding=utf-8 -*-

import os
import pdb
import jionlp as jio


keyword = "觊觎"
dir_path = '/home/cuichengyu/dataset/raw_texts'
file_path = os.path.join(dir_path, 'all_texts_2.txt')


def get_keyword_context(keyword, file_path, boundary=3):
    context_list = list()
    length_keyword = len(keyword)
    for line in jio.read_file_by_iter(file_path):
        if type(line) is not str:
            continue
        if keyword in line:
            a = line.index(keyword)
            # pdb.set_trace()
            context = line[a-boundary: a+length_keyword+boundary]
            context_list.append(context)

    context_list = list(set(context_list))
    return context_list


context_list = get_keyword_context(keyword, file_path)
for line in context_list:
    print(line)
