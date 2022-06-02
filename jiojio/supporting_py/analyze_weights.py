# -*- coding=utf-8 -*-

import os
import pdb
import numpy as np


dir_path = '/home/cuichengyu/github/jiojio/jiojio/models/default_cws_model'


npz = np.load(os.path.join(dir_path, 'weights.npz'))
sizes = npz['sizes']
bi_ratio = np.array(npz['bi_ratio'], dtype=np.float32)

node_weight = npz['node_weight'].astype(np.float16)  # 强制转换 数据类型
edge_weight = npz['edge_weight'].astype(np.float32)  # 强制转换 数据类型

cnt = 0
for i in range(sizes[1]):
    gap = node_weight[i].max() - node_weight[i].min()
    if gap < 4e-3:
        cnt += 1
        # pdb.set_trace()

print(cnt, cnt / sizes[1])
pdb.set_trace()


# sizes = np.array([self.n_tag, self.n_feature])
np.savez(os.path.join(dir_path, 'weights1.npz'),
    sizes=sizes, bi_ratio=bi_ratio,
    node_weight=node_weight, edge_weight=edge_weight)
