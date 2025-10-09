import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def plot_tournament_results(env):  
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    import os

    scores = {agent.name: agent.wealth for agent in env.agents}

    if not os.path.exists("results"):
        os.makedirs("results")

    # --- Total Scores Bar Plot ---
    plt.figure(figsize=(12, 25))  
    plt.barh(list(scores.keys()), list(scores.values()))
    plt.title("Total Scores", fontsize=18)
    plt.xlabel("Wealth", fontsize=14)
    plt.ylabel("Agent", fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    plt.savefig("results/total_scores_bar.png", dpi=300)
    plt.clf()

    # --- Matchup Heatmap ---
    agent_names = [agent.name for agent in env.agents]
    n = len(agent_names)

    heatmap_data = np.zeros((n, n))
    name_to_index = {name: idx for idx, name in enumerate(agent_names)}

    for (player_name, opponent_name), score in env.match_scores.items():
        i = name_to_index[player_name]
        j = name_to_index[opponent_name]
        heatmap_data[i][j] = score

    df = pd.DataFrame(heatmap_data, index=agent_names, columns=agent_names)

    fig, ax = plt.subplots(figsize=(18, 16))  # Larger figure for clarity
    cax = ax.matshow(df.values, cmap='coolwarm')

    # Axis ticks and labels
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(agent_names, rotation=90, fontsize=10, fontweight='bold')
    ax.set_yticklabels(agent_names, fontsize=10, fontweight='bold')

    # Add gridlines for readability
    ax.set_xticks(np.arange(-.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-.5, n, 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=0.2)

    # Titles and colorbar
    plt.title("Matchup Heatmap (Score per Match)", fontsize=18, pad=25)
    cbar = plt.colorbar(cax)
    cbar.ax.tick_params(labelsize=10)
    cbar.set_label("Score", fontsize=12)

    plt.tight_layout()
    plt.savefig("results/heatmap_scores.png", dpi=300, bbox_inches='tight')
    plt.clf()

