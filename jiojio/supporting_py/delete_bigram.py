# -*- coding=utf-8 -*-

import os
import pdb
import json


dir_path = '/home/cuichengyu/github/jiojio/jiojio/models/3500000_model'

with open(os.path.join(dir_path, 'features.json'), 'r', encoding='utf-8') as fr:
    res = json.load(fr)

print(res.keys())
unigram = set(res['unigram'])
bigram = set(res['bigram'])
feature_to_idx = res['feature_to_idx']
tag_to_idx = res['tag_to_idx']

print(len(bigram))
invalid_bigrams = set()
for bi_feature in bigram:
    pre, suf = bi_feature.split('*')
    if (pre not in unigram) or (suf not in unigram):
        invalid_bigrams.add(bi_feature)
print(len(invalid_bigrams), len(invalid_bigrams) / len(bigram))

bigram = bigram - invalid_bigrams
final_res = dict()
final_res = {'unigram': sorted(list(unigram)), 'bigram': sorted(list(bigram)),
             'feature_to_idx': feature_to_idx, 'tag_to_idx': tag_to_idx}
with open(os.path.join(dir_path, 'features.json'), 'w', encoding='utf-8') as fw:
    json.dump(final_res, fw, ensure_ascii=False, indent=4, separators=(',', ':'))
