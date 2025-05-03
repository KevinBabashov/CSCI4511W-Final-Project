from typing import List, Dict
import random

COOPERATE = "C"
DEFECT = "D"
ABSTAIN = "A"

PAYOFFS = {
    (COOPERATE, COOPERATE): (3, 3),
    (DEFECT, DEFECT): (-1, -1),
    (COOPERATE, DEFECT): (-5, 5),
    (DEFECT, COOPERATE): (5, -5),
    (ABSTAIN, ABSTAIN): (0, 0),
    (COOPERATE, ABSTAIN): (0, 0),
    (ABSTAIN, COOPERATE): (0, 0),
    (DEFECT, ABSTAIN): (0, 0),
    (ABSTAIN, DEFECT): (0, 0)
}


class Agent:
    def __init__(self, name: str, strategy_fn=None, trust_model=None):
        self.name = name
        self.strategy = strategy_fn
        self.trust_model = trust_model
        self.history = []
        self.opponent_history = []
        self.wealth = 0
        self.trust = {}
        self.evidence = {}
        self.beliefs = {} 

    def play(self):
        move = self.strategy(self.history, self.opponent_history)
        self.history.append(move)
        return move

    def reset(self):
        self.history = []
        self.opponent_history = []

    def beta_expected_value(self, success: int, fail: int) -> float:
        return (success + 1) / (success + fail + 2)

    def update_beliefs(self, opponent_name: str, action: str):
        if opponent_name not in self.beliefs:
            self.beliefs[opponent_name] = {"C": 1/3, "L": 1/3, "A": 1/3}

        prior = self.beliefs[opponent_name]
        likelihoods = {
            "C": {COOPERATE: 0.8, DEFECT: 0.1, ABSTAIN: 0.1},
            "L": {COOPERATE: 0.2, DEFECT: 0.4, ABSTAIN: 0.4},
            "A": {COOPERATE: 0.1, DEFECT: 0.7, ABSTAIN: 0.2},
        }
        marginal = sum(likelihoods[t][action] * prior[t] for t in prior)
        new_belief = {t: (likelihoods[t][action] * prior[t]) / marginal for t in prior}
        self.beliefs[opponent_name] = new_belief

    def update_trust(self, opponent_name: str, action: str):
        if opponent_name not in self.trust:
            self.trust[opponent_name] = 0.5
        if opponent_name not in self.evidence:
            self.evidence[opponent_name] = {"success": 0, "fail": 0}

        if action == COOPERATE:
            self.evidence[opponent_name]["success"] += 1
        elif action == DEFECT:
            self.evidence[opponent_name]["fail"] += 1

        if action == DEFECT:
            self.trust[opponent_name] -= 0.1
        elif action == COOPERATE:
            self.trust[opponent_name] += 0.1

        self.trust[opponent_name] = max(0, min(1, self.trust[opponent_name]))

    def decide_action(self, opponent: 'Agent', shared_trust: dict) -> str:
        if self.strategy is not None:
            return self.strategy(self.history, opponent.history)

        trust_level = self.trust.get(opponent.name, 0.5)

        if self.trust_model == 1:
            own_ev = self.evidence.get(opponent.name, {"success": 0, "fail": 0})
            trust_level = self.beta_expected_value(own_ev["success"], own_ev["fail"])

        elif self.trust_model == 2:
            own_ev = self.evidence.get(opponent.name, {"success": 0, "fail": 0})
            own_trust = self.beta_expected_value(own_ev["success"], own_ev["fail"])
            shared_value = shared_trust.get(opponent.name, 0.5)
            recommender_trust = shared_trust.get("RecommenderAgent", 0.5)
            trust_level = (own_trust + shared_value * recommender_trust) / (1 + recommender_trust)

        elif self.trust_model == 3:
            trust_level = shared_trust.get(opponent.name, 0.5)

        elif self.trust_model == 4:
            beliefs = self.beliefs.get(opponent.name, {"C": 1/3, "L": 1/3, "A": 1/3})
            expected_cooperation = 0.8 * beliefs["C"] + 0.2 * beliefs["L"] + 0.1 * beliefs["A"]
            if beliefs["A"] > 0.6:
                return ABSTAIN
            elif expected_cooperation < 0.3:
                return DEFECT
            else:
                return COOPERATE

        elif self.trust_model == 5:
            if len(opponent.history) == 0:
                return DEFECT  # Start by defecting
            elif opponent.history[-1] == COOPERATE:
                return DEFECT  # Exploit cooperation
            elif opponent.history[-1] == DEFECT:
                return DEFECT if self.history.count(COOPERATE) > 0 else COOPERATE  # Escalate retaliation


        if trust_level < 0.3:
            return ABSTAIN
        elif trust_level < 0.5:
            return DEFECT
        else:
            return COOPERATE


class Environment:
    def __init__(self, agents, rounds=100):
        self.agents = agents
        self.rounds = rounds
        self.wealth_history = {agent.name: [] for agent in agents}
        self.match_scores = {}

    def run(self):
        for agent in self.agents:
            agent.wealth = 0
            agent.history = []
        self.wealth_history = {agent.name: [] for agent in self.agents}

        for _ in range(self.rounds):
            for i, agent1 in enumerate(self.agents):
                for j, agent2 in enumerate(self.agents):
                    if i >= j:
                        continue
                    self.play_round(agent1, agent2)
                    # Record wealth after every interaction
                    for agent in self.agents:
                        self.wealth_history[agent.name].append(agent.wealth)

    def play_round(self, agent1: Agent, agent2: Agent):
        shared_trust = self.calculate_shared_trust()

        action1 = agent1.decide_action(agent2, shared_trust)
        action2 = agent2.decide_action(agent1, shared_trust)

        payoff1, payoff2 = PAYOFFS[(action1, action2)]

        agent1.wealth += payoff1
        agent2.wealth += payoff2

        key1 = (agent1.name, agent2.name)
        key2 = (agent2.name, agent1.name)

        if key1 not in self.match_scores:
            self.match_scores[key1] = 0
        if key2 not in self.match_scores:
            self.match_scores[key2] = 0

        self.match_scores[key1] += payoff1
        self.match_scores[key2] += payoff2

        if action1 != ABSTAIN:
            agent1.update_trust(agent2.name, action2)
            agent1.update_beliefs(agent2.name, action2)
        if action2 != ABSTAIN:
            agent2.update_trust(agent1.name, action1)
            agent2.update_beliefs(agent1.name, action1)

    def calculate_shared_trust(self) -> Dict[str, float]:
        trust_scores: Dict[str, List[float]] = {}
        for agent in self.agents:
            for other_name, ev in agent.evidence.items():
                val = (ev["success"] + 1) / (ev["success"] + ev["fail"] + 2)
                trust_scores.setdefault(other_name, []).append(val)

        shared_trust = {name: sum(values) / len(values) for name, values in trust_scores.items()}
        return shared_trust

    def results(self):
        sorted_agents = sorted(
            [(agent.name, agent.wealth) for agent in self.agents],
            key=lambda x: -x[1]
        )
        return "\n".join([f"{name}: {wealth}" for name, wealth in sorted_agents])
