import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import seaborn as sns
import plotly.graph_objects as go
import networkx as nx

# Load Data
bar_data = pd.read_csv("bar_assignment.csv")
sankey_data = pd.read_csv("sankey_assignment.csv")
network_data = pd.read_csv("networks_assignment.csv")  

plt.rcParams.update({
    "font.family": "Arial", 
    "font.size": 16          
})

# --- BAR CHART ---
bar_data["COUNT"] = bar_data["COUNT"].map({1: "Yes", 0: "No"})
pivot_table = bar_data.pivot_table(index="LABEL", columns="COUNT", aggfunc="size", fill_value=0)

yes_counts = pivot_table["Yes"]
no_counts = pivot_table["No"]

plt.figure(figsize=(8, 6))
bars1 = plt.barh(pivot_table.index, no_counts, color="red", label="No")
bars2 = plt.barh(pivot_table.index, yes_counts, left=no_counts, color="blue", label="Yes")

for bars in [bars1, bars2]:
    for bar in bars:
        width = bar.get_width()
        if width > 0:
            plt.text(bar.get_x() + width / 2, bar.get_y() + bar.get_height() / 2, int(width),
                     ha="center", va="center", fontsize=12, fontweight="bold", color="white")

plt.xlabel("Count")
plt.ylabel("Category")
plt.title("Horizontal Stacked Bar Chart")
plt.xticks([0, 2, 4, 6, 8, 10])
plt.legend(title="Response")
plt.savefig("Bar Chart.png")

plt.show() 

# --- SANKEY DIAGRAM ---
first_layer_sources = ["PS", "OMP", "CNP", "NRP", "NMCCC", "PEC", "NCDM", "RGS"]
final_layer_targets = ["Reg", "Aca", "Oth"]
source, target, value = [], [], []

for src in first_layer_sources:
    for i, label in enumerate(sankey_data["LABEL"]):
        source.append(src)
        target.append(label)
        value.append(sankey_data[src][i])

for tgt in final_layer_targets:
    for i, label in enumerate(sankey_data["LABEL"]):
        source.append(label)
        target.append(tgt)
        value.append(sankey_data[tgt][i])

all_nodes = list(dict.fromkeys(source + target))
node_indices = {node: i for i, node in enumerate(all_nodes)}

sankey = go.Figure(go.Sankey(
    node=dict(
        pad=15, thickness=20, line=dict(color="black", width=0.5),
        label=all_nodes,
        color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"] * 3
    ),
    link=dict(
        source=[node_indices[s] for s in source],
        target=[node_indices[t] for t in target],
        value=value,
        color="rgba(150,150,150,0.4)"
    )
))

sankey.write_image("Sankey Diagram.png")
sankey.show()

# --- NETWORK GRAPH ---
G = nx.Graph()
central_nodes = ["D", "F", "I", "N", "S"]
blue_nodes = central_nodes
green_nodes = ['BIH', 'GEO', 'ISR', 'MNE', 'SRB', 'CHE', 'TUR', 'UKR', 'GBR', 'AUS', 'HKG', 'USA']
yellow_nodes = ['AUT', 'BEL', 'BGR', 'HRV', 'CZE', 'EST', 'FRA', 'DEU', 'GRC', 'HUN', 'IRL', 'ITA', 'LVA', 'LUX', 'NLD', 'PRT', 'ROU', 'SVK', 'SVN', 'ESP']
node_colors = {n: "blue" for n in blue_nodes}
node_colors.update({n: "green" for n in green_nodes})
node_colors.update({n: "yellow" for n in yellow_nodes})

for col in network_data.columns[1:]:
    for index, row in network_data.iterrows():
        if row[col] > 0:
            G.add_edge(row["LABELS"], col)

plt.figure(figsize=(10, 10))
pos = nx.shell_layout(G, nlist=[central_nodes, list(G.nodes - set(central_nodes))])
nx.draw(G, pos, with_labels=True, node_color=[node_colors.get(n, "gray") for n in G.nodes], edge_color="gray", node_size=500)
plt.savefig("Network Plot.png")

plt.show()  

# --- COLLATE VISUALIZATIONS ---
fig = plt.figure(figsize=(16, 12))
gs = GridSpec(2, 2, width_ratios=[1, 1], height_ratios=[1, 1])

bar_ax = fig.add_subplot(gs[0, 0])
sankey_ax = fig.add_subplot(gs[1, 0])
network_ax = fig.add_subplot(gs[:, 1])  


bar_img = plt.imread("Bar Chart.png")
sankey_img = plt.imread("Sankey Diagram.png")
network_img = plt.imread("Network Plot.png")


bar_ax.imshow(bar_img)
bar_ax.axis("off")
bar_ax.set_title("Bar Chart", fontsize=16, fontweight="bold")


sankey_ax.imshow(sankey_img)
sankey_ax.axis("off")
sankey_ax.set_title("Sankey", fontsize=16, fontweight="bold")


network_ax.imshow(network_img)
network_ax.axis("off")
network_ax.set_title("Network Plot", fontsize=16, fontweight="bold")

fig.suptitle("Collated Visualization", fontsize=18, fontweight="bold")

plt.savefig("Collated Visualization.pdf")
plt.show()