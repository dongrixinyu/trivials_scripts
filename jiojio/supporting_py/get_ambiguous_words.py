# -*- coding=utf-8 -*-

import os

import pdb
import json
from collections import Counter

import jionlp as jio


dir_path = '/home/cuichengyu/dataset'
file_path = os.path.join(dir_path, 'cws.txt')
words_path = '/home/cuichengyu/words_freq.json'


def get_ambiguous_words(file_path, words_path, ratio=0.1):

    with open(words_path, 'r', encoding='utf-8') as fr:
        words_dict = json.load(fr)

    print('length of words dict: ', len(words_dict))

    count_dict = dict([(word, 0) for word, freq in words_dict.items()])
    bigram_dict = Counter()
    for words in jio.read_file_by_iter(file_path): #,line_num=10000):
        if type(words) is not list:
            continue
        # pdb.set_trace()
        for pre, suf in zip(words[:-1], words[1:]):
            if pre in words_dict:
                flag = False
                for i in range(3, 0, -1):
                    ambigu = pre[-1] + suf[:i]
                    if ambigu in words_dict:
                        flag = True
                        break

                if flag:
                    # print(pre, suf, ambigu)
                    bigram_dict.update([pre + '+' + suf])
                    count_dict[pre] += 1
                    # pdb.set_trace()

            if suf in words_dict:
                flag = False
                for i in range(3, 0, -1):
                    ambigu = pre[len(pre) - i:] + suf[0]
                    if ambigu in words_dict:
                        flag = True
                        break

                if flag:
                    # print(pre, suf, ambigu)
                    # pdb.set_trace()
                    bigram_dict.update([pre + '+' + suf])
                    count_dict[suf] += 1

    print('total bigram num: ', len(bigram_dict))
    # pdb.set_trace()
    total_bigram_num = sum([freq for _, freq in bigram_dict.most_common()])
    res = dict([(word, freq) for word, freq in bigram_dict.most_common() if freq > 10])
    print('# final {:.2%} features are saved.'.format(
        sum([freq for word, freq in res.items()]) / total_bigram_num))
    print('# final true feature_num: {}'.format(len(res)))

    return res, count_dict


bigrams, _ = get_ambiguous_words(file_path, words_path, ratio=0.1)

with open('/home/cuichengyu/bigram_freq.json', 'w', encoding='utf-8') as fw:
    json.dump(bigrams, fw, ensure_ascii=False, indent=4, separators=(',', ':'))
