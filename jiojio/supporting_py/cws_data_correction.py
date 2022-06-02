# -*- coding=utf-8 -*-

import os
import pdb
import json
import jionlp as jio

dir_path = '/home/cuichengyu/dataset/cws'

word_list = ['区块链']
chinese_idioms = jio.chinese_idiom_loader()
word_list = [idiom for idiom in chinese_idioms if chinese_idioms[idiom]['freq'] > 2]

dc_with_words = jio.cws.CWSDCWithStandardWords(word_list)
with open(os.path.join(dir_path, 'sentences_tuned.txt'), 'w', encoding='utf-8') as fw:
    for idx, sample in enumerate(jio.read_file_by_iter(os.path.join(dir_path, 'sentences.txt'))):
        # try:
        res = dc_with_words(sample, verbose=True)
        # pdb.set_trace()
        fw.write(json.dumps(res, ensure_ascii=False) + '\n')
        # except:
        #
        # if '区块链' in res:
        #     print(res)
        #     pdb.set_trace()
