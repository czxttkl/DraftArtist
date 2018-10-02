import optparse
import sys


def parse_mcts_exp_parameters():
    if len(sys.argv) < 2:
        print('no argument set. use default.')
        return None

    parser = optparse.OptionParser(usage="usage: %prog [options]")

    parser.add_option("--num_matches", dest="num_matches", type="int", default=0)
    parser.add_option("--p0", dest="p0", type="string", default='')
    parser.add_option("--p1", dest="p1", type="string", default='')
    (kwargs, args) = parser.parse_args()
    return kwargs


def parse_mcts_maxiter_c(player_str):
    assert player_str.startswith('mcts')
    _, maxiter, c = player_str.split('_')
    return int(maxiter), float(c)


def parse_rave_maxiter_c_k(player_str):
    assert player_str.startswith('rave')
    _, maxiter, c, k = player_str.split('_')
    return int(maxiter), float(c), float(k)

