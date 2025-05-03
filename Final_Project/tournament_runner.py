import os
from Game_Playing import Agent, Environment
from strategies import deterministic_strategies, stochastic_strategies, deceptive_strategies, probing_strategies, evolutionary_strategies, group_aware_strategies
from strategies.utility import plot_tournament_results

all_strategies = (
    deterministic_strategies.all_strategies +
    stochastic_strategies.all_strategies +
    deceptive_strategies.all_strategies +
    probing_strategies.all_strategies +
    evolutionary_strategies.all_strategies +
    group_aware_strategies.all_strategies
)

# Setup agents
trust_agents = [
        Agent("PersonalTrust", trust_model=1),
        Agent("TRAVOSTrust", trust_model=2),
        Agent("HearsayTrust", trust_model=3),
        Agent("DefectiveAgent", trust_model=4),
        Agent("AdversaryAgent", trust_model=5),
    ]

agents = [Agent(name=s.__name__, strategy_fn=s) for s in all_strategies]
agents += trust_agents

# Setup environment
env = Environment(agents, rounds=50)

# Run tournament
env.run()

# Plot and save results
if not os.path.exists("results"):
    os.makedirs("results")

plot_tournament_results(env)
