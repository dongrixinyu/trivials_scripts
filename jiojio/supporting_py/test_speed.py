# -*- coding=utf-8 -*-


import os
import json
import numpy as np
import jionlp as jio


model_dir_path = '/home/cuichengyu/github/jiojio/jiojio/models/default_model'

weight_file_path = os.path.join(model_dir_path, 'weights.npz')
features_json_path = os.path.join(model_dir_path, 'features.json')

npz = np.load(weight_file_path)
sizes = npz["sizes"]
node_weight = npz["node_weight"].astype(np.float32)  # 强制转换 数据类型

# 特征值
with open(features_json_path, 'r', encoding='utf-8') as fr:
    features_json = json.load(fr)


times = 10000000
dicter = features_json['feature_to_idx']

with jio.TimeIt('pure for loop') as ti:
    for i in range(times):
        pass
    pure_time = ti.break_point()

with jio.TimeIt('test dict') as ti:
    for i in range(times):
        a = 'kkk' in dicter
    dict_time = ti.break_point()

setter = set(list(features_json['feature_to_idx'].keys()))
with jio.TimeIt('test set') as ti:
    for i in range(times):
        c = 'kkk' in setter
    set_time = ti.break_point()

print('{:.2%}'.format((dict_time - set_time) / (set_time - pure_time)))
print(a,c)
