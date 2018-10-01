"""
used to read mcts_result.csv
usage example: python result_reader.py mcts_200_0.03125 mcts_100_1
"""
import optparse
parser = optparse.OptionParser(usage="usage: %prog [options]")
(kwargs, args) = parser.parse_args()
p0_query, p1_query = args[0], args[1]
p0_wr_pick_first, p0_wr_pick_second = 0, 0

file = 'mcts_result.csv'

for line in open(file, 'r'):
    _, _, p0, p1, wr, _ = line.split(',')
    try:
        p0, p1, wr = p0.strip(), p1.strip(), float(wr.strip())
    except:
        continue
    if p0 == p0_query and p1 == p1_query:
        p0_wr_pick_first = wr
    if p0 == p1_query and p1 == p0_query:
        p0_wr_pick_second = 1 - wr

print('p0 pick first wr:', p0_wr_pick_first)
print('p0 pick second wr:', p0_wr_pick_second)
print('po average wr: {:.3f}'.format((p0_wr_pick_first + p0_wr_pick_second) / 2))
