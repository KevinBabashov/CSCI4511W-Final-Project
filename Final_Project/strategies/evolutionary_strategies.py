
def adaptive_majority(history, opponent_history):
    if len(opponent_history) < 5:
        return 'C'
    recent = opponent_history[-5:]
    return 'C' if recent.count('C') >= 3 else 'D'

def trend_follower(history, opponent_history):
    if len(history) == 0:
        return 'C'
    if history[-1] == 'C':
        return 'C'
    return 'D'

def evolver(history, opponent_history):
    if len(opponent_history) < 3:
        return 'C'
    if opponent_history[-1] == 'C' and opponent_history[-2] == 'C':
        return 'C'
    if opponent_history[-1] == 'D' and opponent_history[-2] == 'D':
        return 'D'
    return 'C'

def persistent_tft(history, opponent_history):
    if not opponent_history:
        return 'C'
    return 'C' if opponent_history[-1] == 'C' else 'D'

def revenge_seeker(history, opponent_history):
    if 'D' in opponent_history[-5:]:
        return 'D'
    return 'C'

def flexible_grudger(history, opponent_history):
    if opponent_history.count('D') > opponent_history.count('C'):
        return 'D'
    return 'C'

def cautious_trend(history, opponent_history):
    if len(history) < 2:
        return 'C'
    if opponent_history[-1] == opponent_history[-2]:
        return opponent_history[-1]
    return 'C'


all_strategies = [
    adaptive_majority,
    trend_follower,
    evolver,
    persistent_tft,
    revenge_seeker,
    flexible_grudger,
    cautious_trend,
]
