# -*- coding=utf-8 -*-

# 删除包含异常字符的文本，主要是编码错误的文本

import os
import re
import pdb
import jionlp as jio


exception_list = list()

pattern = r'|'.join(exception_list)
# chinese_pattern = re.compile('[]')
pattern = re.compile(r'(' + pattern + r')')

# pdb.set_trace()
file_path = '/home/cuichengyu/dataset/bosson/all_tuned_pos.json'
clean_list = list()

r_list = ['TA们', 'Ta们', 'ta们', 'tA们']
for idx, line in enumerate(jio.read_file_by_iter(file_path)):
    if type(line) is not list:
        continue

    if idx % 100000 == 0:
        print(idx)

    is_exception = False
    for word, tag in zip(line[0], line[1]):
        # pdb.set_trace()
        if tag == 'nx':
            # print(word, '\t', tag)
            is_exception = True
            break

    if not is_exception:
        # pdb.set_trace()
        clean_list.append(line)
    else:
        new_tag_list = list()
        for word, tag in zip(line[0], line[1]):
            if tag == 'nx':
                if word in r_list:
                    print(word)
                    new_tag_list.append('r')
                else:
                    new_tag_list.append('n')
            else:
                new_tag_list.append(tag)
        clean_list.append([line[0], new_tag_list])

    # if not jio.check_chinese_char(text):  # 全文无中文
        # print(text)
        # pdb.set_trace()
    #     continue


    # if pattern.search(text) is None:
    #     clean_list.append(line)
    # else:
        # print(text)
        # pdb.set_trace()
    #     pass

print(list(set(exception_list)))
print(len(clean_list))
jio.write_file_by_line(
    clean_list, '/home/cuichengyu/dataset/bosson/all_tuned_pos1.json')
