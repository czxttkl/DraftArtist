"""
Generate hero win rate distribution, which will be used for a baseline strategy
"""
import pickle
from collections import defaultdict
import numpy
import pprint

data_path = '../../input/dota.pickle'
output_path = 'dota_win_rate_dist.pickle'
select_dist = defaultdict(int)
win_rate_dist = defaultdict(int)

with open(data_path, 'rb') as f:
    M_o, M_r_C, M_b_C, match_id2idx_dict, hero_id2idx_dict, Z, M = pickle.load(f)
    for i in range(Z):
        if i % 1000 == 0:
            print(i)
        for c in M_r_C[i]:
            select_dist[c] += 1
            if M_o[i]:
                win_rate_dist[c] += 1
        for c in M_b_C[i]:
            select_dist[c] += 1
            if not M_o[i]:
                win_rate_dist[c] += 1

print('select dist:')
pprint.pprint(select_dist)
print('win rate dist:')
pprint.pprint(win_rate_dist)

with open(output_path, 'wb') as f:
    p = numpy.zeros(M)
    for i in range(M):
        print(i)
        print(win_rate_dist[i])
        print(select_dist[i])
        if select_dist[i] == 0:
            continue
        p[i] = win_rate_dist[i] / select_dist[i]
    print('p', p)
    pickle.dump(p, f)
