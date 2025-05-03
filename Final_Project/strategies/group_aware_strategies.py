import random


def forgiving_majority(history, opponent_history):
    return 'C' if opponent_history.count('C') >= opponent_history.count('D') - 1 else 'D'

def harsh_majority(history, opponent_history):
    return 'D' if opponent_history.count('D') >= opponent_history.count('C') else 'C'

def tft_in_small_groups(history, opponent_history):
    return 'C' if opponent_history.count('C') > opponent_history.count('D') else 'D'

def nice_tft(history, opponent_history):
    return 'C' if opponent_history.count('C') >= opponent_history.count('D') else 'D'

def skeptical_majority(history, opponent_history):
    if opponent_history.count('D') > opponent_history.count('C') + 1:
        return 'D'
    return 'C'

def cooperative_majority(history, opponent_history):
    if opponent_history.count('C') >= opponent_history.count('D'):
        return 'C'
    return 'D'


all_strategies = [
    forgiving_majority,
    harsh_majority,
    tft_in_small_groups,
    nice_tft,
    skeptical_majority,
    cooperative_majority,
]
