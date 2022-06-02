# -*- coding=utf-8 -*-

import os
import pdb
import json
import numpy as np
from collections import Counter

dir_path = '/home/cyy/github/jiojio/jiojio/models/test_pos_model'

weight_path = os.path.join(dir_path, 'weights.npz')

npz = np.load(weight_path)
sizes = npz['sizes']
bi_ratio = np.array(npz['bi_ratio'], dtype=np.float16)

node_weight = npz['node_weight'].astype(np.float16)
edge_weight = npz['edge_weight'].astype(np.float16)


# 调整 features.json 的权重
features_file = os.path.join(dir_path, 'features.json')
with open(features_file, 'r', encoding='utf-8') as fr:
    features_json = json.load(fr)

_unigram = features_json['unigram']
_char = features_json['char']
_part = features_json['part']
_single_pos_word = features_json['single_pos_word']
_feature_to_idx = features_json['feature_to_idx']
_tag_to_idx = features_json['tag_to_idx']
idx_to_feature = dict([(value, key) for key, value in _feature_to_idx.items()])



count = 0
full_count = 0
suppress_index_list = dict()
new_node_weight = list()  #np.empty(sizes, dtype=np.float16)
for i in range(sizes[1]):
    print(idx_to_feature[i])
    count_dict = sorted(Counter(node_weight[i]).items(), key=lambda i: i[0])
    tmp_node_weight = np.sort(node_weight[i])

    num_num = sum([i[1] for i in count_dict[1:]])
    if num_num == 1:
        count += 1
        assert tmp_node_weight[-2] == tmp_node_weight[0]
        suppress_index_list.update(
            {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())]]})

    elif num_num == 2:
        count += 1
        assert tmp_node_weight[-3] == tmp_node_weight[0]

        if tmp_node_weight[-2] - tmp_node_weight[-3] <= 0.001:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())]]})
        else:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())],
                                         [str(tmp_node_weight[-2]), str(np.where(node_weight[i] == tmp_node_weight[-2])[0][0])]]})
        print('length num: 2', i)
        print(suppress_index_list[i])
        print(node_weight[i])
        # pdb.set_trace()

    elif num_num == 3:
        count += 1
        assert tmp_node_weight[-4] == tmp_node_weight[0]

        if tmp_node_weight[-2] - tmp_node_weight[-4] <= 0.001:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())]]})
        elif tmp_node_weight[-3] - tmp_node_weight[-4] <= 0.001:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())],
                                         [str(tmp_node_weight[-2]), str(np.where(node_weight[i] == tmp_node_weight[-2])[0][0])]]})
        else:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())],
                                         [str(tmp_node_weight[-2]), str(np.where(node_weight[i] == tmp_node_weight[-2])[0][0])],
                                         [str(tmp_node_weight[-3]), str(np.where(node_weight[i] == tmp_node_weight[-3])[0][0])]]})

        print('length num: 3', i)
        print(suppress_index_list[i])
        print(node_weight[i])
        # pdb.set_trace()
    elif num_num == 4:
        count += 1
        assert tmp_node_weight[-5] == tmp_node_weight[0]

        if tmp_node_weight[-2] - tmp_node_weight[-5] <= 0.001:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())]]})
        elif tmp_node_weight[-3] - tmp_node_weight[-5] <= 0.001:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())],
                                         [str(tmp_node_weight[-2]), str(np.where(node_weight[i] == tmp_node_weight[-2])[0][0])]]})
        elif tmp_node_weight[-4] - tmp_node_weight[-5] <= 0.001:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())],
                                         [str(tmp_node_weight[-2]), str(np.where(node_weight[i] == tmp_node_weight[-2])[0][0])],
                                         [str(tmp_node_weight[-3]), str(np.where(node_weight[i] == tmp_node_weight[-3])[0][0])]]})
        else:
            suppress_index_list.update(
                {i: [str(tmp_node_weight[0]), [str(node_weight[i].max()), str(node_weight[i].argmax())],
                                         [str(tmp_node_weight[-2]), str(np.where(node_weight[i] == tmp_node_weight[-2])[0][0])],
                                         [str(tmp_node_weight[-3]), str(np.where(node_weight[i] == tmp_node_weight[-3])[0][0])],
                                         [str(tmp_node_weight[-4]), str(np.where(node_weight[i] == tmp_node_weight[-4])[0][0])]]})

        print('length num: 4', i)
        print(suppress_index_list[i])
        print(node_weight[i])
        # pdb.set_trace()
    elif num_num == 5:
        print('length num: 5', i)
        # print(suppress_index_list[i])
        print(tmp_node_weight)
        print(node_weight[i])
        # pdb.set_trace()
    else:
        # print(tmp_node_weight)
        new_node_weight.append(node_weight[i])
        pass
        # pdb.set_trace()
    if len(set(tmp_node_weight)) > 20:
        full_count += 1

print(sizes[1])
print(count, count / sizes[1])
print(full_count, full_count / sizes[1])

with open(os.path.join(dir_path, 'suppress.json'), 'w', encoding='utf-8') as fw:
    json.dump(suppress_index_list, fw, ensure_ascii=False)

weight_path = os.path.join(dir_path, 'weights_tune.npz')
new_node_weight = np.concatenate([np.expand_dims(i, axis=1) for i in new_node_weight], axis=1)
# pdb.set_trace()
np.savez(weight_path, sizes=sizes, bi_ratio=bi_ratio,
        node_weight=new_node_weight, edge_weight=edge_weight)
