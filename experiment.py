import sys
sys.path.insert(0, '..')

import random
import numpy as np
import time
import logging
from utils.parser import parse_mcts_exp_parameters
from captain_mode_draft import Draft


def experiment(match_id, p0_model_str, p1_model_str, env_path):
    t1 = time.time()
    d = Draft(env_path, p0_model_str, p1_model_str)  # instantiate board

    while not d.end():
        p = d.get_player()
        t2 = time.time()
        # whether it is ban or pick
        mt = d.decide_move_type()
        a = p.get_move(mt)
        d.move(a)
        d.print_move(match_id=match_id, move_duration=time.time() - t2, move_id=a, move_type=mt)

    final_red_team_win_rate = d.eval()
    duration = time.time() - t1
    exp_str = 'match: {}, time: {:.3F}, red team predicted win rate: {:.5f}' \
        .format(match_id, duration, final_red_team_win_rate)

    return final_red_team_win_rate, duration, exp_str


if __name__ == '__main__':
    random.seed(123)
    np.random.seed(123)
    # win rate predictor path
    env_path = 'NN_hiddenunit120_dota.pickle'

    logger = logging.getLogger('mcts')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.WARNING)

    kwargs = parse_mcts_exp_parameters()
    # possible player string: random, hwr, mcts_maxiter_c, assocrule
    # red team
    p0_model_str = 'hwr' if not kwargs else kwargs.p0
    # blue team
    p1_model_str = 'mcts_200_0.5' if not kwargs else kwargs.p1
    num_matches = 30 if not kwargs else kwargs.num_matches

    red_team_win_rates, times = [], []
    for i in range(num_matches):
        wr, t, s = experiment(i, p0_model_str, p1_model_str, env_path)
        red_team_win_rates.append(wr)
        times.append(t)
        s += ', mean predicted win rate: {:.5f}\n'.format(np.average(red_team_win_rates))
        logger.warning(s)

    logger.warning('{} matches, {} vs. {}. average time {:.5f}, average red team win rate {:.5f}, std {:.5f}'
                   .format(num_matches, p0_model_str, p1_model_str,
                           np.average(times), np.average(red_team_win_rates), np.std(red_team_win_rates)))
