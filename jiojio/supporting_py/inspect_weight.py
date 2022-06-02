# -*- coding=utf-8 -*-

import os
import pdb
import sys
import json
import numpy as np


model_dir_path = '/home/cuichengyu/github/jiojio/jiojio/models/3500000_model'

weight_file_path = os.path.join(model_dir_path, 'weights.npz')
features_json_path = os.path.join(model_dir_path, 'features.json')

npz = np.load(weight_file_path)
sizes = npz["sizes"]
node_weight = npz["node_weight"].astype(np.float32)  # 强制转换 数据类型
edge_weight = npz["edge_weight"].astype(np.float32)  # 强制转换 数据类型

# 特征值
with open(features_json_path, 'r', encoding='utf-8') as fr:
    features_json = json.load(fr)


def get_feature_weight(feature_name):
    print('feature_name: ', feature_name)
    idx = features_json['feature_to_idx'][feature_name]
    print('feature_weight: ', node_weight[idx])


def get_feature_type_weight(feature_type):
    all_weight = np.array([0., 0.])
    total_num = 0
    num = 0

    def compute(all_weight, num, total_num, i):
        all_weight += np.absolute(node_weight[features_json['feature_to_idx'][i]])
        item = node_weight[features_json['feature_to_idx'][i]]
        if item[0] - item[1] <= 0.001 and item[1] - item[0] <= 0.001:
            num += 1
            # print(item)
            # pdb.set_trace()
        total_num += 1
        return all_weight, num, total_num

    for i in features_json['feature_to_idx']:
        if feature_type == 'a':
            if i.startswith(feature_type):
                if not i.startswith('ac'):
                    all_weight, num, total_num = compute(all_weight, num, total_num, i)

        elif feature_type == 'b':
            if i.startswith(feature_type):
                if not i.startswith('bc'):
                    all_weight, num, total_num = compute(all_weight, num, total_num, i)
        elif feature_type == 'c':
            if i.startswith(feature_type):
                if not i.startswith('cd') and not i.startswith('ce') and not i.startswith('cf'):
                    all_weight, num, total_num = compute(all_weight, num, total_num, i)
        else:
            if i.startswith(feature_type):
                all_weight, num, total_num = compute(all_weight, num, total_num, i)
                # pdb.set_trace()

    print('# ', feature_type, total_num, all_weight / total_num, '{:.2%}'.format(num / total_num))


while True:
    string = input('input the feature:')
    get_feature_weight(string)

sys.exit()
get_feature_type_weight('zc')
get_feature_type_weight('a')
get_feature_type_weight('ac')
get_feature_type_weight('b')
get_feature_type_weight('bc')
get_feature_type_weight('c')
get_feature_type_weight('cd')
get_feature_type_weight('d')
get_feature_type_weight('ce')
get_feature_type_weight('e')
get_feature_type_weight('cf')

get_feature_type_weight('wl')
get_feature_type_weight('wr')
get_feature_type_weight('v')
get_feature_type_weight('x')
# pdb.set_trace()
