import pdb
import os
import numpy as np


dir_path = '/home/cyy/github/jiojio/jiojio/models/default_pos_model'

weight_file = os.path.join(dir_path, 'weights.npz')

# 调整 weights.npz 权重
npz = np.load(weight_file)
sizes = npz['sizes']
bi_ratio = np.array(npz['bi_ratio'], dtype=np.float16)

node_weight = npz['node_weight'].astype(np.float16)
edge_weight = npz['edge_weight'].astype(np.float16)

node_weight[0] = node_weight[0] / 4
# pdb.set_trace()

if True:
    dir_path = '/home/cyy/github/jiojio/jiojio/models/default_pos_model'

    weight_file = os.path.join(dir_path, 'weights.npz')
    features_file = os.path.join(dir_path, 'features.json')

    sizes = np.array([sizes[0], node_weight.shape[0]])
    print(sizes)
    np.savez(weight_file, sizes=sizes, bi_ratio=bi_ratio,
        node_weight=node_weight, edge_weight=edge_weight)
