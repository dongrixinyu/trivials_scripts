# -*- coding=utf-8 -*-

# 去重

import os

import pdb
import json
import random
import hashlib
import jionlp as jio

from jionlp.gadget.trie_tree import TrieTree

file_path = '/home/cuichengyu/dataset/bosson/sentences.txt'
file_path = '/home/cuichengyu/dataset/cws/sentences.txt'

trie_tree_obj = TrieTree()
duplicate_res_list = list()
md5_length = 10

play_city = 0

# with open('/home/cuichengyu/dataset/bosson/dupli_sentences.txt', 'w', encoding='utf-8') as fw:
if True:
    for idx, line in enumerate(jio.read_file_by_iter(
            file_path)): #, auto_loads_json=False, strip=True, line_num=1000000)):

        # if '娱乐城' in line:  # 此比例过大，要压缩
        #     if random.random() > 0.03:
        #         continue
        pure_line = ''.join(line)
        # pdb.set_trace()
        # if '娱乐城' in pure_line:
        #     if pure_line.count('彩票') > 40:
        #         continue
        #     play_city += 1

        has_chinese = jio.check_chinese_char(pure_line)
        if not has_chinese:
            continue

        key = hashlib.md5(pure_line.encode('utf-8')).hexdigest()[:md5_length]

        _, res = trie_tree_obj.search(key)

        if res is None:
            trie_tree_obj.add_node(key, str(idx))
            duplicate_res_list.append(json.dumps(line, ensure_ascii=False))
            # fw.write(json.dumps(line, ensure_ascii=False) + '\n')
        else:
            # 匹配到重复，丢弃该数据
            assert _ == md5_length
            # print(res, idx)  # 历史数据值
            # pdb.set_trace()

        if idx % 1000000 == 0:
            print(idx)

print(play_city)
print(idx)
# print(len(duplicate_res_list))

random.shuffle(duplicate_res_list)

jio.write_file_by_line(
    duplicate_res_list, '/home/cuichengyu/dataset/cws/dupli_sentences.txt')
