import random

def prober(history, opponent_history):
    probe_sequence = ['D', 'C', 'C']
    if len(history) < len(probe_sequence):
        return probe_sequence[len(history)]
    if 'D' in opponent_history[:3]:
        return opponent_history[-1]
    return 'D'

def deceitful_grim(history, opponent_history):
    if len(history) == 0:
        return 'C'
    if 'D' in opponent_history:
        return 'D'
    if len(history) % 5 == 0:
        return 'D'
    return 'C'

def double_agent(history, opponent_history):
    if len(history) < 10:
        return 'C'
    return 'D'

def fake_forgiver(history, opponent_history):
    if len(history) % 7 == 0:
        return 'D'
    return 'C'

def manipulator(history, opponent_history):
    if len(opponent_history) > 0 and opponent_history[-1] == 'D':
        return 'C'
    return 'D'

def sneak_attack(history, opponent_history):
    if len(history) < 5:
        return 'C'
    if random.random() < 0.2:
        return 'D'
    return 'C'

all_strategies = [
    prober,
    deceitful_grim,
    double_agent,
    fake_forgiver,
    manipulator,
    sneak_attack,
]
