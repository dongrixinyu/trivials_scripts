# -*- coding=utf-8 -*-

# 统计 cws.txt 分词文件中的所有词汇，并统计词频

import os
import re
import pdb
import json
from collections import Counter
import jionlp as jio


dir_path = '/home/cuichengyu/dataset'
file_path = os.path.join(dir_path, 'cws.txt')

num_pattern = re.compile('^\d+(,\d+)?(\.\d+)?(万|亿|万亿|万千|千|点|亿千|兆)$')


# pdb.set_trace()
def get_words_list(file_path, trim_num=80):  # 词频过低将有大量的人名
    words_dict = Counter()
    for line in jio.read_file_by_iter(file_path):
        if type(line) is not list:
            continue
        # pdb.set_trace()
        words_dict.update(line)

    print('# orig feature num: {}'.format(len(words_dict)))
    total_words_num = sum([freq for _, freq in words_dict.most_common()])
    print('# total word nums: {}'.format(total_words_num))

    print('# {:.2%} features are saved.'.format(
        sum([freq for _, freq in words_dict.most_common()
             if freq > trim_num]) / sum(list(words_dict.values()))))

    feature_set = [(feature, freq) for feature, freq in words_dict.most_common()
                   if freq > trim_num]

    print('# true feature_num: {}'.format(len(feature_set)))

    res = dict()
    for word, freq in feature_set:
        if freq < trim_num:
            continue
        if not jio.check_chinese_char(word):
            continue
        if len(word) >= 10:
            continue
        if num_pattern.search(word) is not None:
            continue
        if '@' in word or '，' in word or '·' in word:
            continue

        if freq < 800:
            if jio.ner.check_person_name(word):
                # print(word)
                # pdb.set_trace()
                continue

        res.update({word: freq})

    print('# final {:.2%} features are saved.'.format(
        sum([freq for word, freq in res.items()]) / total_words_num))
    print('# final true feature_num: {}'.format(len(res)))
    return res


res = get_words_list(file_path)
dirname = os.path.dirname(__file__)
with open(os.path.join(dirname, 'words_freq.json'), 'w', encoding='utf-8') as fw:
    json.dump(res, fw, ensure_ascii=False, indent=4, separators=(',', ':'))
