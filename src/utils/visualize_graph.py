import sys
sys.path.append("../environment/")

import torch
import networkx as nx
import matplotlib.pyplot as plt
from environment import Environment

def visualize_network(network):
    # Create a NetworkX graph
    G = nx.Graph()

    # Create a mapping from node indices to their positions
    pos = {}
    for node_id, node in network.nodes.items():
        G.add_node(node_id, node_type=node.node_type, capacity=node.capacity, staff=node.staff, demand=node.demand)
        pos[node_id] = (node.coordinates[1].item(), node.coordinates[0].item())  # Use attributes from Node objects

    for arc_id, (arc, source, target) in network.arcs.items():
        G.add_edge(source, target, length=arc.length, travel_time=arc.travel_time, capacity=arc.capacity,
                   traffic_condition=arc.traffic_condition, safety=arc.safety, usage_cost=arc.usage_cost, open=arc.open)

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    
    # Add edge labels
    edge_labels = {(u, v): f"{d['length']:.1f}, {d['travel_time']:.1f}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Transport Network Graph")
    plt.show()

if __name__ == "__main__":
    # Load the TransportNetwork object
    network = Environment()
    pyg_data = torch.load("../../data/generated/environment.pth")
    network.from_pyg_data(pyg_data)
    
    print("Graph loaded from transport_network.pth")
    
    # Print out nodes and their coordinates for debugging
    for node_id, node in network.nodes.items():
        print(f"Node {node_id}: coordinates={node.coordinates}")
    
    visualize_network(network)
