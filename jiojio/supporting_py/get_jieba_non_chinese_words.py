# -*- coding=utf-8 -*-

import os
import jionlp as jio
from jiojio import read_file_by_iter, write_file_by_line

file_1_path = '/home/cuichengyu/github/jieba/extra_dict/dict.txt.big'
file_2_path = '/home/cuichengyu/github/jieba/jieba/dict.txt'

word_list = list()
for line in read_file_by_iter(file_1_path):
    word, _, _ = line.strip().split(' ')
    has_chinese = jio.check_chinese_char(word)
    if not has_chinese:
        word_list.append(word)

for line in read_file_by_iter(file_2_path):
    word, _, _ = line.strip().split(' ')
    has_chinese = jio.check_chinese_char(word)
    if not has_chinese:
        word_list.append(word)

write_file_by_line(list(set(word_list)),
                   '/home/cuichengyu/github/jiojio/supporting_py/non_chinese_words.txt')
