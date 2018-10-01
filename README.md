# DraftArtist

`This repo is still under construction. Expected to complete in Oct 10th, 2018`

Example code for [
The Art of Drafting: A Team-Oriented Hero Recommendation System for Multiplayer Online Battle Arena Games](https://arxiv.org/abs/1806.10130)

Authors: Zhengxing Chen, Truong-Huy D Nguyen, Yuyu Xu, Chris Amato, Seth Cooper, Yizhou Sun, Magy Seif El-Nasr

### Usage
The code shows our algorithm for hero recommendation in [Captain Mode](https://dota2.gamepedia.com/g00/Game_modes?i10c.encReferrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8%3D&i10c.ua=1#Captains_Mode).

The command line to simulate drafts between two teams (p0 & p1) according to Algorithm 1 in the paper is:  
```
python3.6 experiment.py --num_matches=NUM_MATCHS --p0=STRATEGY0 --p1=STRATEGY1 
```
`num_matches` specifies how many drafts to simulate. The first player's first draft is always randomized in each match. The rule of randomized first pick is: regardless of the strategy adopted, the first hero
is sampled following the probability distribution reflecting how frequently each hero is picked in our dataset. 

Possible strategy strings are:
* `random`: randomly draft heroes
* `hwr`: always pick the hero not drafted yet and with the highest win rate
* `mcts_maxiter_c`: Monte Carlo Tree Search-based drafting, with `maxiter` iterations and exploration term `c`
* `assocrule`: association rule-based drafting

### Examples
```
python3.6 experiment.py --num_matches=500 --p0=mcts_800_0.5 --p1=mcts_400_0.5 
```

```
python3.6 experiment.py --num_matches=500 --p0=mcts_800_0.5 --p1=assocrule 
```

### Files
`models` several models used in MCTS simulation

* `hero_win_rates.pickle` a dictionary recording each hero's win rate in our dataset. key: hero index, value: the win rate with value in (0, 1)
* `NN_hiddenunit120_dota.pickle` a neural network model trained by scikit-learn, used to predict win rate given a completed draft
* `hero_freqs.pickle` a dictionary recording each hero's selection frequency in our dataset. key: hero index, value: selection frequency normalized in (0, 1).

`utils` utility files

### Requirement

Python 3.6. Please also see `requirements.txt`