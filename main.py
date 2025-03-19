# Imports
import random
import networkx as nx
import matplotlib.pyplot as plt

# Create a Wireless Sensor Network (WSN) graph
G = nx.DiGraph()
nodes = range(1, 11)
base_station = 0

# Add nodes and base station
G.add_node(base_station, type="base_station")
for node in nodes:
    G.add_node(node, type="sensor")

# Randomly connect nodes to simulate communication links
for node in nodes:
    neighbors = random.sample([n for n in nodes if n != node], k=2)
    for neighbor in neighbors:
        G.add_edge(node, neighbor, weight=random.randint(1, 10))

# Connect all nodes to the base station
for node in nodes:
    G.add_edge(node, base_station, weight=random.randint(5, 15))

# Visualize the WSN with enhanced clarity
def draw_graph(G, malicious_node=None):
    pos = nx.spring_layout(G, seed=42)
    colors = []
    for node in G.nodes():
        if node == 0:
            colors.append("red") 
        elif node == malicious_node:
            colors.append("orange")
        else:
            colors.append("blue")
    
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=500, font_size=8, font_color="white")
    nx.draw_networkx_edges(G, pos, edge_color="gray", alpha=0.5)
    plt.title("Wireless Sensor Network")
    plt.show()

# Evaluate baseline metrics
def evaluate_baseline(G):
    total_paths = 0
    valid_paths = 0
    for node in nodes:
        if nx.has_path(G, node, base_station):
            total_paths += 1
            valid_paths += 1  # All paths are valid since no malicious node
    print("Baseline Evaluation:")
    print(f"Total paths: {total_paths}")
    print(f"Valid paths: {valid_paths}")
    baseline_ratio = (valid_paths / total_paths) * 100
    print(f"Packet delivery ratio (baseline): {baseline_ratio:.2f}%\n")
evaluate_baseline(G)

# Simulate a sinkhole attack
malicious_node = random.choice(nodes)
def simulate_sinkhole_attack(G, malicious_node):
    print(f"Malicious node: {malicious_node}")
    for neighbor in list(G.neighbors(malicious_node)):
        G[malicious_node][neighbor]["weight"] = 1  # Advertise fake low cost
simulate_sinkhole_attack(G, malicious_node)
draw_graph(G, malicious_node)

# Evaluate post-attack metrics
def evaluate_with_security(G, malicious_node, apply_security=False):
    total_paths = 0
    valid_paths = 0
    for node in nodes:
        if nx.has_path(G, node, base_station):
            total_paths += 1
            if malicious_node not in nx.shortest_path(G, node, base_station):
                valid_paths += 1

    if apply_security:
        print("Post-Security Evaluation:")
    else:
        print("Post-Attack Evaluation:")

    print(f"Total paths: {total_paths}")
    print(f"Valid paths: {valid_paths}")
    security_ratio = (valid_paths / total_paths) * 100
    print(f"Packet delivery ratio: {security_ratio:.2f}%\n")

evaluate_with_security(G, malicious_node)

# Intrusion Detection System (IDS)
def intrusion_detection_system(G):
    flagged_nodes = []
    for node in nodes:
        outgoing_edges = G.out_degree(node)
        if outgoing_edges > 10:
            flagged_nodes.append(node)
    print(f"IDS flagged nodes: {flagged_nodes}")
    return flagged_nodes

# Apply secure routing to mitigate sinkhole attack
def secure_routing(G, malicious_node):
    for node in nodes:
        if nx.has_path(G, node, base_station):
            path = nx.shortest_path(G, node, base_station)
            if malicious_node in path:
                if G.has_edge(node, malicious_node):
                    G.remove_edge(node, malicious_node)
    print("Secure routing applied. Malicious node paths removed.")

secure_routing(G, malicious_node)

evaluate_with_security(G, malicious_node, apply_security=True)

# Simulate energy usage
def simulate_energy_usage(G):
    energy_consumption = {node: random.uniform(0.5, 2.0) for node in nodes}  # Random energy per node
    total_energy = sum(energy_consumption.values())
    print(f"Total energy consumption: {total_energy:.2f} units")
    return total_energy

baseline_energy = simulate_energy_usage(G)

# Simulate latency
def simulate_latency(G):
    latency = []
    for node in nodes:
        if nx.has_path(G, node, base_station):
            path = nx.shortest_path_length(G, node, base_station, weight="weight")
            latency.append(path)
    avg_latency = sum(latency) / len(latency) if latency else 0
    print(f"Average latency: {avg_latency:.2f} ms")
    return avg_latency

baseline_latency = simulate_latency(G)
