
def always_cooperate(history, opponent_history):
    return 'C'

def always_defect(history, opponent_history):
    return 'D'

def tit_for_tat(history, opponent_history):
    if not opponent_history:
        return 'C'
    return opponent_history[-1]

def grudger(history, opponent_history):
    if 'D' in opponent_history:
        return 'D'
    return 'C'

def forgiver(history, opponent_history):
    if not opponent_history:
        return 'C'
    if opponent_history[-1] == 'C':
        return 'C'
    return 'D'

def snob(history, opponent_history):
    if len(opponent_history) < 3:
        return 'C'
    return 'D' if opponent_history[-1] == 'D' else 'C'

def slow_tit_for_tat(history, opponent_history):
    if len(opponent_history) < 3:
        return 'C'
    return opponent_history[-1]

def win_stay_lose_shift(history, opponent_history):
    if len(history) == 0:
        return 'C'
    if history[-1] == 'C' and opponent_history[-1] == 'C':
        return 'C'
    return 'D'

def soft_majority(history, opponent_history):
    return 'C' if opponent_history.count('C') > opponent_history.count('D') else 'D'

def hard_majority(history, opponent_history):
    return 'C' if opponent_history.count('C') >= opponent_history.count('D') else 'D'

def cooperative_tft(history, opponent_history):
    if len(history) == 0:
        return 'C'
    return opponent_history[-1]

def anti_tft(history, opponent_history):
    if len(history) == 0:
        return 'D'
    return opponent_history[-1]

def grim_trigger(history, opponent_history):
    if 'D' in opponent_history:
        return 'D'
    return 'C'

def retaliator(history, opponent_history):
    if len(opponent_history) == 0:
        return 'C'
    return 'D' if opponent_history[-1] == 'D' else 'C'

def suspicious_tft(history, opponent_history):
    if not opponent_history:
        return 'D'
    return opponent_history[-1]

def grudging_tft(history, opponent_history):
    if 'D' in opponent_history:
        return 'D'
    if not opponent_history:
        return 'C'
    return opponent_history[-1]

all_strategies = [
    always_cooperate,
    always_defect,
    tit_for_tat,
    grudger,
    forgiver,
    snob,
    slow_tit_for_tat,
    win_stay_lose_shift,
    soft_majority,
    hard_majority,
    cooperative_tft,
    anti_tft,
    grim_trigger,
    retaliator,
    suspicious_tft,
    grudging_tft,
]
