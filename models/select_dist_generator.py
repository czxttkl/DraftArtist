"""
Generate hero selection distribution, which will be used for sampling the first hero
"""
import pickle
from collections import defaultdict
import numpy
import pprint

data_path = '../../input/dota.pickle'
output_path = 'dota_select_dist.pickle'
select_dist = defaultdict(int)

with open(data_path, 'rb') as f:
    M_o, M_r_C, M_b_C, match_id2idx_dict, hero_id2idx_dict, Z, M = pickle.load(f)
    for i in range(Z):
        if i % 1000 == 0:
            print(i)
        for c in M_r_C[i]:
            select_dist[c] += 1
        for c in M_b_C[i]:
            select_dist[c] += 1

pprint.pprint(select_dist)

with open(output_path, 'wb') as f:
    a = numpy.arange(M)
    p = numpy.zeros(M)
    for i in range(M):
        p[i] = select_dist[i]
    p = p / numpy.sum(p)
    print('a', a)
    print('p', p)
    pickle.dump((a, p), f)
