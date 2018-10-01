from math import log, sqrt


class Node:
    """
    maintains state of nodes in
    the monte carlo search tree
    """

    def __init__(self, parent=None, action=None, player=None, untried_actions=None, c=None):
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried_actions = untried_actions
        self.action = action
        self.player = player
        self.c = c

    def select(self):
        """
        select child of node with
        highest UCB1 value
        """
        s = sorted(self.children, key=lambda c: c.wins / c.visits + 0.2 * self.c * sqrt(log(self.visits) / c.visits))
        return s[-1]

    def select_final(self):
        """
        select the best move as result, without exploration term.
        """
        s = sorted(self.children, key=lambda c: c.wins / c.visits)
        return s[-1].action

    def expand(self, action, player, untried_actions):
        """
        expand parent node (self) by adding child
        node with given action and state
        """
        child = Node(parent=self, action=action, player=player, untried_actions=untried_actions, c=self.c)
        self.untried_actions.remove(action)
        self.children.append(child)
        return child

    def update(self, result):
        """
        result is a real-valued number (i.e., predicted win rate of player 0) in our case
        """
        self.visits += 1
        self.wins += result