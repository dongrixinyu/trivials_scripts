# -*- coding=utf-8 -*-

import os
import pdb
import json
import numpy as np


dir_path = '/home/cyy/github/jiojio/jiojio/models/test_cws_model'

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
_bigram = features_json['bigram']
_feature_to_idx = features_json['feature_to_idx']
_tag_to_idx = features_json['tag_to_idx']

print('max val: ', max(list(_feature_to_idx.values())))
# '''
idx_to_feature = dict([(value, key) for key, value in _feature_to_idx.items()])

# 删减不明显的特征，减少大约 1.6%
weight_gap = 0.0001  # np.float16 精度的最低限
new_idx_to_feature = dict()
new_node_weight_list = list()
delete_list = list()
for idx in range(node_weight.shape[0]):

    if node_weight[idx].max() - node_weight[idx].min() < weight_gap:
        # 权重分布均匀，无较大的区分度
        # if cur_weight_mean * 10 <= weight_mean:
        #     # 当前平均权重不足总平均权重的 十分之一
        #     params_being_cut.append(idx_to_feature[idx])
        #     continue
        delete_list.append(idx)
        continue

    new_idx_to_feature.update({idx: idx_to_feature[idx]})
    new_node_weight_list.append(idx)
# '''

new_feature_to_idx = dict([(value, idx) for idx, (key, value) in enumerate(new_idx_to_feature.items())])
# feature_to_idx = [(key, idx) for idx, (key, val) in enumerate(_feature_to_idx.items())]
print('feature_to_idx num: ', len(_feature_to_idx))
print('weight_num:         ', node_weight.shape[0])
print('new feature num: ', len(new_node_weight_list))
print('saved {:.3%}'.format((node_weight.shape[0] - len(new_node_weight_list)) / node_weight.shape[0]))
node_weight = node_weight[new_node_weight_list]

pdb.set_trace()

# 重新调整 node_weight 的压缩
opposite_diff_dict = dict()
for idx in range(node_weight.shape[0]):
    tmp_node_weight = node_weight[idx]
    if abs(tmp_node_weight[0] + tmp_node_weight[1]) > weight_gap:
        tmp_list = list()
        tmp_list.append('{:.4f}'.format(float(tmp_node_weight[0])))
        tmp_list.append('{:.4f}'.format(float(tmp_node_weight[1])))
        opposite_diff_dict.update({idx: tmp_list})
        print(tmp_node_weight)
        pdb.set_trace()

new_node_weight = node_weight[:, 0]

print('opposite num: {}, percent: {:.3%}'.format(
    len(opposite_diff_dict), len(opposite_diff_dict) / len(new_node_weight_list)))


pdb.set_trace()

if True:
    dir_path = '/home/cyy/github/jiojio/jiojio/models/default_cws_model'

    weight_file = os.path.join(dir_path, 'weights1.npz')
    features_file = os.path.join(dir_path, 'features1.json')
    opposite_diff_file = os.path.join(dir_path, 'opposite_diff.json')

    sizes = np.array([sizes[0], new_node_weight.shape[0]])
    print(sizes)
    np.savez(weight_file, sizes=sizes, bi_ratio=bi_ratio,
        node_weight=new_node_weight, edge_weight=edge_weight)

    # 写入新文件 opposite_diff.json
    with open(opposite_diff_file, 'w', encoding='utf-8') as fw:
        json.dump(opposite_diff_dict, fw, ensure_ascii=False)#, indent=4, separators=(',', ':'))

    # 写入新文件 feature.json
    data = dict()
    data['unigram'] = sorted(list(_unigram))
    data['bigram'] = sorted(list(_bigram))
    data['feature_to_idx'] = list(new_feature_to_idx.keys())
    data['tag_to_idx'] = _tag_to_idx
    print(len(new_feature_to_idx))
    with open(features_file, 'w', encoding='utf-8') as fw:
        json.dump(data, fw, ensure_ascii=False)#, indent=4, separators=(',', ':'))
