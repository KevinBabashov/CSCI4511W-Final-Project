import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def plot_wealth_over_time(wealth_history):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(16, 9))

    for name, history in wealth_history.items():
        plt.plot(history, label=name)

    plt.xlabel("Number of Interactions", fontsize=14)
    plt.ylabel("Cumulative Wealth", fontsize=14)
    plt.title("Agent Wealth Over Time (Per Interaction)", fontsize=16)
    plt.grid(True)

    # Legend positioned below the plot in a multi-column table format
    plt.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.25),
        ncol=6,         # adjust this number depending on how many methods you have
        fontsize=9,
        frameon=False
    )

    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.show()



def plot_tournament_results(env):  
    scores = {agent.name: agent.wealth for agent in env.agents}

    if not os.path.exists("results"):
        os.makedirs("results")

    plt.figure(figsize=(12, 25))  
    plt.barh(list(scores.keys()), list(scores.values()))
    plt.title("Total Scores")
    plt.tight_layout()
    plt.savefig("results/total_scores_bar.png")
    plt.clf()

    agent_names = [agent.name for agent in env.agents]
    n = len(agent_names)

    heatmap_data = np.zeros((n, n))
    name_to_index = {name: idx for idx, name in enumerate(agent_names)}

    for (player_name, opponent_name), score in env.match_scores.items():
        i = name_to_index[player_name]
        j = name_to_index[opponent_name]
        heatmap_data[i][j] = score

    df = pd.DataFrame(heatmap_data, index=agent_names, columns=agent_names)

    fig, ax = plt.subplots(figsize=(14, 12)) 
    cax = ax.matshow(df.values, cmap='coolwarm') 

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(agent_names, rotation=90, fontsize=6)
    ax.set_yticklabels(agent_names, fontsize=6)
    plt.title("Matchup Heatmap (Score per Match)", pad=20)
    plt.colorbar(cax)
    plt.tight_layout()
    plt.savefig("results/heatmap_scores.png")
    plt.clf() 
