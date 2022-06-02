# -*- coding=utf-8 -*-

import os
import pdb
import json
import jionlp as jio


dir_path = '/home/cyy/datasets/pos'
file_name_template = 'pos_sentences_{}.txt'

for i in range(3):
    file_path = os.path.join(dir_path, file_name_template.format(i))
    with open(file_path + '.cor', 'w', encoding='utf-8') as fw:
        for idx, line in enumerate(jio.read_file_by_iter(file_path)):
            # print(line)
            # pdb.set_trace()
            new_line = [[word, tag] for word, tag in zip(line[0], line[1])]
            new_line = json.dumps(new_line, ensure_ascii=False) + '\n'
            fw.write(new_line)
            # pdb.set_trace()
















print('finished!')
