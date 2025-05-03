import random

# ======================
# Probing Strategies
# ======================

def strategic_probe(history, opponent_history):
    sequence = ['C', 'D', 'C', 'D']
    if len(history) < len(sequence):
        return sequence[len(history)]
    return opponent_history[-1]

def detective(history, opponent_history):
    probe_sequence = ['C', 'D', 'C', 'C']
    if len(history) < len(probe_sequence):
        return probe_sequence[len(history)]
    if 'D' in opponent_history[:4]:
        return 'D'
    return opponent_history[-1]

def invasive_probe(history, opponent_history):
    if len(history) < 3:
        return 'D'
    if opponent_history.count('D') > opponent_history.count('C'):
        return 'D'
    return 'C'

def annoyed_probe(history, opponent_history):
    if len(opponent_history) < 2:
        return 'C'
    if opponent_history[-1] == 'D' and opponent_history[-2] == 'D':
        return 'D'
    return 'C'

def suspicious_probe(history, opponent_history):
    if len(history) == 0:
        return 'D'
    return opponent_history[-1]

# ======================
# List of Strategies
# ======================

all_strategies = [
    strategic_probe,
    detective,
    invasive_probe,
    annoyed_probe,
    suspicious_probe,
]
