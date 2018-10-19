# DraftArtist

Example code for [
The Art of Drafting: A Team-Oriented Hero Recommendation System for Multiplayer Online Battle Arena Games](https://dl.acm.org/citation.cfm?id=3240345)

Authors: Zhengxing Chen, Truong-Huy D Nguyen, Yuyu Xu, Chris Amato, Seth Cooper, Yizhou Sun, Magy Seif El-Nasr

Point of Contact: Zhengxing Chen, czxttkl@gmail.com
### Usage
The code shows our algorithm for hero recommendation in DOTA 2 [Captain Mode](https://dota2.gamepedia.com/g00/Game_modes?i10c.encReferrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8%3D&i10c.ua=1#Captains_Mode).

Below is the command line to simulate drafts between two teams (p0 & p1) according to Algorithm 1 in the paper:  
```
python3.6 experiment.py --num_matches=NUM_MATCHS --p0=STRATEGY0 --p1=STRATEGY1 
```
`num_matches` specifies how many drafts to simulate. The first team's first draft is always randomized in each match. The rule of randomized first pick is: regardless of the strategy adopted, the first hero
is sampled following the probability distribution reflecting how frequently each hero is picked in our dataset. 

Possible strategy strings are:
* `random`: randomly draft heroes
* `hwr`: always pick the hero not drafted yet and with the highest win rate
* `mcts_maxiter_c`: Monte Carlo Tree Search-based drafting, with `maxiter` iterations and exploration term `c`
* `assocrule`: association rule-based drafting

### Examples
```
# Simulate 500 matches, with the first team adopting MCTS with 100 iterations and 0.03125 exploration strength, 
# and the second team adopting the association rule-based strategy:
python3.6 experiment.py --num_matches=500 --p0=mcts_100_0.03125 --p1=assocrule 
# Result
500 matches, p0 mcts_100_0.03125 vs. p1 assocrule. average time 2.09252, average p0 win rate 0.68968, std 0.15239 
```

```
# Simulate 500 matches, with the first team adopting the association rule-based strategy,
# and the second team adopting MCTS with 100 iterations and 0.03125 exploration strength:
python3.6 experiment.py --num_matches=500 --p0=assocrule --p1=mcts_100_0.03125 
# Result
500 matches, p0 assocrule vs. p1 mcts_100_0.03125. average time 2.12751, average p0 win rate 0.32866, std 0.15362 
```
[0.68968 + (1 - 0.32866)] / 2 = 0.68051, which is close to what we report (0.686) for UCT_100,0.03125 vs. AR in Table 5. (Results vary a little depending on the random seed being used) 

### Files
`apriori` relevant files for the association rule-based strategy.
* `dota_lose_team_output.txt` hero combinations appear frequently in the same losing team 
* `dota_oppo_team_output.txt` hero combinations appear frequently in opposite teams
* `dota_win_team_output.txt` hero combinations appear frequently in the same winning team

`input` input file folder
* `dota.pickle` contains the processed dataset of 3 million matches from "Performance of machine learning algorithms in predicting
game outcome from drafts in Dota 2" (Semenov et al., 2016). 

`models` several models used in MCTS simulation

* `hero_win_rates.pickle` a dictionary recording each hero's win rate in our dataset. key: hero index, value: the win rate with value in (0, 1)
* `NN_hiddenunit120_dota.pickle` a neural network model trained by scikit-learn, used to predict win rate given a completed draft
* `hero_freqs.pickle` a dictionary recording each hero's selection frequency in our dataset. key: hero index, value: selection frequency normalized in (0, 1).

`utils` utility files

`experiment.py` the main file to start simulation

`node.py` implements MCTS-based simulation (UCT specifically)

`captain_mode_draft.py` implements the specific drafting rules of Captain Mode

`player.py` implements different team drafting strategies

### Requirement

Python 3.6. Please also see `requirements.txt`
