import random
from node import Node
import logging
import numpy
import pickle

logger = logging.getLogger('mcts')


class Player:

    def get_first_move(self):
        with open('models/hero_freqs.pickle', 'rb') as f:
            a, p = pickle.load(f)
            return numpy.random.choice(a, size=1, p=p)[0]

    def get_move(self, move_type):
        raise NotImplementedError


class RandomPlayer(Player):

    def __init__(self, draft):
        self.draft = draft
        self.name = 'random'

    def get_move(self, move_type):
        """
        decide the next move
        """
        if self.draft.if_first_move():
            return self.get_first_move()
        moves = self.draft.get_moves()
        return random.sample(moves, 1)[0]


class HighestWinRatePlayer(Player):

    def __init__(self, draft):
        self.draft = draft
        self.name = 'hwr'
        with open('models/hero_win_rates.pickle', 'rb') as f:
            self.win_rate_dist = pickle.load(f)

    def get_move(self, move_type):
        """
        decide the next move
        """
        if self.draft.if_first_move():
            return self.get_first_move()
        moves = self.draft.get_moves()
        move_win_rates = [(m, self.win_rate_dist[m]) for m in moves]
        best_move, best_win_rate = sorted(move_win_rates, key=lambda x: x[1])[-1]
        return best_move


class MCTSPlayer(Player):

    def __init__(self, name, draft, maxiters, c):
        self.draft = draft
        self.name =name
        self.maxiters = maxiters
        self.c = c

    def get_move(self, move_type):
        """
        decide the next move
        """
        if self.draft.if_first_move():
            return self.get_first_move()

        root = Node(player=self.draft.player, untried_actions=self.draft.get_moves(), c=self.c)

        for i in range(self.maxiters):
            node = root
            tmp_draft = self.draft.copy()

            # selection - select best child if parent fully expanded and not terminal
            while len(node.untried_actions) == 0 and node.children != []:
                # logger.info('selection')
                node = node.select()
                tmp_draft.move(node.action)
            # logger.info('')

            # expansion - expand parent to a random untried action
            if len(node.untried_actions) != 0:
                # logger.info('expansion')
                a = random.sample(node.untried_actions, 1)[0]
                tmp_draft.move(a)
                p = tmp_draft.player
                node = node.expand(a, p, tmp_draft.get_moves())
            # logger.info('')

            # simulation - rollout to terminal state from current
            # state using random actions
            while not tmp_draft.end():
                # logger.info('simulation')
                moves = tmp_draft.get_moves()
                a = random.sample(moves, 1)[0]
                tmp_draft.move(a)
            # logger.info('')

            # backpropagation - propagate result of rollout game up the tree
            # reverse the result if player at the node lost the rollout game
            while node != None:
                # logger.info('backpropagation')
                if node.player == 0:
                    result = tmp_draft.eval()
                else:
                    result = 1 - tmp_draft.eval()
                node.update(result)
                node = node.parent
            # logger.info('')

        return root.select_final()


class AssocRulePlayer(Player):

    def __init__(self, draft):
        self.draft = draft
        self.name = 'assocrule'
        self.load_rules(match_num=3056596,
                        oppo_team_spmf_path='apriori/dota_oppo_team_output.txt',
                        win_team_spmf_path='apriori/dota_win_team_output.txt',
                        lose_team_spmf_path='apriori/dota_lose_team_output.txt')

    def load_rules(self, match_num, oppo_team_spmf_path, win_team_spmf_path, lose_team_spmf_path):
        self.oppo_1_rules = dict()
        self.oppo_2_rules = dict()
        with open(oppo_team_spmf_path, 'r') as f:
            for line in f:
                items, support = line.split(' #SUP: ')
                items, support = list(map(int, items.strip().split(' '))), int(support.strip())
                # S(-e), because -e is losing champion encoded in 1xxx
                if len(items) == 1 and items[0] > 1000:
                    self.oppo_1_rules[frozenset(items)] = support / match_num
                elif len(items) == 2 and (items[0] < 1000 and items[1] > 1000):
                    self.oppo_2_rules[frozenset(items)] = support / match_num
                else:
                    continue

        self.win_rules = dict()
        with open(win_team_spmf_path, 'r') as f:
            for line in f:
                items, support = line.split(' #SUP: ')
                items, support = list(map(int, items.strip().split(' '))), int(support.strip())
                if len(items) == 1:
                    continue
                self.win_rules[frozenset(items)] = support / match_num

        self.lose_rules = dict()
        with open(lose_team_spmf_path, 'r') as f:
            for line in f:
                items, support = line.split(' #SUP: ')
                items, support = list(map(int, items.strip().split(' '))), int(support.strip())
                if len(items) == 1:
                    continue
                self.lose_rules[frozenset(items)] = support / match_num

    def get_move(self, move_type):
        if self.draft.if_first_move():
            return self.get_first_move()

        player = self.draft.next_player
        # if ban, we are selecting the best hero for opponent
        if move_type == 'ban':
            player = player ^ 1
        allies = frozenset(self.draft.get_state(player))
        oppo_player = player ^ 1
        # enemy id needs to add 1000
        enemies = frozenset([i+1000 for i in self.draft.get_state(oppo_player)])

        R = list()

        ally_candidates = list()
        for key in self.win_rules:
            intercept = allies & key
            assoc = key - intercept
            if len(intercept) > 0 and len(assoc) == 1:
                assoc = next(iter(assoc))  # extract the move from the set
                if assoc in self.draft.get_moves():
                    win_sup = self.win_rules[key]
                    lose_sup = self.lose_rules.get(key, 0.0)   # lose support may not exist
                    win_rate = win_sup / (win_sup + lose_sup)
                    ally_candidates.append((allies, key, assoc, win_rate))
        # select top 5 win rate association rules
        ally_candidates = sorted(ally_candidates, key=lambda x: x[-1])[-5:]
        R.extend([a[-2] for a in ally_candidates])

        enemy_candidates = list()
        for key in self.oppo_2_rules:
            intercept = enemies & key
            assoc = key - intercept
            if len(intercept) == 1 and len(assoc) == 1:
                assoc = next(iter(assoc))       # extract the move from the set
                if assoc in self.draft.get_moves():
                    confidence = self.oppo_2_rules[key] / self.oppo_1_rules[intercept]
                    enemy_candidates.append((enemies, key, assoc, confidence))
        # select top 5 confidence association rules
        enemy_candidates = sorted(enemy_candidates, key=lambda x: x[-1])[-5:]
        R.extend([e[-2] for e in enemy_candidates])

        if len(R) == 0:
            moves = self.draft.get_moves()
            return random.sample(moves, 1)[0]
        else:
            move = random.choice(R)
            return move
