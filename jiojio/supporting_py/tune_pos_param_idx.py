# -*- coding=utf-8 -*-

import os
import re
import pdb
import json
import numpy as np


dir_path = '/home/cyy/github/jiojio/jiojio/models/test_pos_model'

weight_file = os.path.join(dir_path, 'weights.npz')
features_file = os.path.join(dir_path, 'features.json')

# 调整 weights.npz 权重
npz = np.load(weight_file)
sizes = npz['sizes']
bi_ratio = np.array(npz['bi_ratio'], dtype=np.float16)

node_weight = npz['node_weight'].astype(np.float16)
edge_weight = npz['edge_weight'].astype(np.float16)


# 调整 features.json 的权重
with open(features_file, 'r', encoding='utf-8') as fr:
    features_json = json.load(fr)

_unigram = features_json['unigram']
_char = features_json['char']
_part = features_json['part']
_single_pos_word = features_json['single_pos_word']
_feature_to_idx = features_json['feature_to_idx']
_tag_to_idx = features_json['tag_to_idx']


bi_part_part_pattern = re.compile('(alcr|blcr|crdl|crel|arcr|brcr|crdr|crer|alcl|blcl|cldl|clel|arcl|brcl|cldr|cler)')
bi_word_part_pattern = re.compile('(alw|blw|wdl|wel|arw|brw|wdr|wer)')
bi_part_word_pattern = re.compile('(ucl|vcl|clx|cly|ucr|vcr|crx|cry)')
# '''
idx_to_feature = dict([(value, key) for key, value in _feature_to_idx.items()])

weight_gap = 0.0019
new_idx_to_feature = dict()
new_node_weight_list = list()
gap_list = list()
for idx in range(node_weight.shape[0]):
    # cur_weight_mean = node_weight[idx].mean()
    gap_list.append(float(node_weight[idx].max() - node_weight[idx].min()))
    if node_weight[idx].max() - node_weight[idx].min() < weight_gap * 2:
        # 大多数为过于特例化的特征，直接过滤掉
        # print(idx_to_feature[idx])
        continue
    elif node_weight[idx].max() - node_weight[idx].min() < weight_gap * 3:
        # print(idx_to_feature[idx])
        if bi_part_part_pattern.match(idx_to_feature[idx]):
            # pdb.set_trace()
            continue
        elif bi_word_part_pattern.match(idx_to_feature[idx]):
            # pdb.set_trace()
            continue
        elif bi_part_word_pattern.match(idx_to_feature[idx]):
            # pdb.set_trace()
            continue
        else:
            pass
    elif node_weight[idx].max() - node_weight[idx].min() < weight_gap * 4:
        # print(idx_to_feature[idx])
        if bi_part_part_pattern.match(idx_to_feature[idx]):
            # pdb.set_trace()
            continue
        elif bi_part_word_pattern.match(idx_to_feature[idx]):
            # pdb.set_trace()
            continue
        else:
            pass
    elif node_weight[idx].max() - node_weight[idx].min() < weight_gap * 5:
        # print(idx_to_feature[idx])
        if bi_part_part_pattern.match(idx_to_feature[idx]):
            # pdb.set_trace()
            continue
        else:
            pass
    new_idx_to_feature.update({idx: idx_to_feature[idx]})
    new_node_weight_list.append(idx)
# '''

new_feature_to_idx = [value for idx, (key, value) in enumerate(new_idx_to_feature.items())]
# feature_to_idx = [(key, idx) for idx, (key, val) in enumerate(_feature_to_idx.items())]
gap_list = sorted(gap_list)
print('mean gap: ', sum(gap_list) / len(gap_list))
print('feature_to_idx num: ', len(_feature_to_idx))
print('weight_num:         ', node_weight.shape[0])
print('new feature num: ', len(new_node_weight_list))
print('saved {:.3%}'.format((node_weight.shape[0] - len(new_node_weight_list)) / node_weight.shape[0]))
node_weight = node_weight[new_node_weight_list]


pdb.set_trace()

if True:
    dir_path = '/home/cyy/github/jiojio/jiojio/models/default_pos_model'

    weight_file = os.path.join(dir_path, 'weights.npz')
    features_file = os.path.join(dir_path, 'features.json')

    sizes = np.array([sizes[0], node_weight.shape[0]])
    print(sizes)
    np.savez(weight_file, sizes=sizes, bi_ratio=bi_ratio,
        node_weight=node_weight, edge_weight=edge_weight)

    print(len(new_feature_to_idx))
    # 写入新文件 feature.json
    data = dict()
    data['unigram'] = sorted(list(_unigram))
    data['char'] = sorted(list(_char))
    data['part'] = sorted(list(_part))
    data['single_pos_word'] = sorted(list(_single_pos_word))
    data['feature_to_idx'] = new_feature_to_idx
    data['tag_to_idx'] = _tag_to_idx
    print(len(new_feature_to_idx))
    with open(features_file, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, ensure_ascii=False, indent=4, separators=(',', ':'))
