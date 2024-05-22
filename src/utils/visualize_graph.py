import sys
sys.path.append("../../")

import torch
import networkx as nx
import matplotlib.pyplot as plt
from torch_geometric.utils import to_networkx
from src.environment.transport_network import TransportNetwork

def visualize_network(network):
    # Convert the transport network to PyTorch Geometric Data object
    pyg_data = network.to_pyg_data()

    # Convert PyTorch Geometric Data object to NetworkX graph
    G = to_networkx(pyg_data, to_undirected=True, node_attrs=['x'], edge_attrs=['edge_attr'])

    # Create a mapping from node indices to their positions
    pos = {}
    for node_id, node in network.nodes.items():
        pos[node_id] = (node.longitude, node.latitude)  # Use attributes from Node objects
    
    # Ensure pos uses integer node indices used by NetworkX
    pos = {i: pos[node_id] for i, node_id in enumerate(network.nodes)}

    # Draw the graph
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    edge_labels = { (u, v): f"{data['edge_attr'][0]:.1f}, {data['edge_attr'][1]:.1f}" for u, v, data in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.title("Transport Network Graph")
    plt.show()



if __name__ == "__main__":
    import pandas as pd
    # Load the TransportNetwork object
    network = TransportNetwork()
    pyg_data = torch.load("../../data/generated/transport_network.pth")
    ## Obtenir le nombre de nœuds
    #num_nodes = pyg_data.num_nodes
#
    ## Obtenir les indices des bords (arcs)
    #edge_index = pyg_data.edge_index.numpy()
#
    ## Liste des node_id pour chaque nœud
    #node_ids = list(range(num_nodes))
#
    ## Créer une liste des paires (source, target) pour chaque arc
    #source_nodes = edge_index[0]
    #target_nodes = edge_index[1]
    #arc_sources_targets = list(zip(source_nodes, target_nodes))
#
    ## Affichage des résultats
    #print("Node IDs pour chaque nœud :", node_ids)
    #print("Pairs (source, target) pour chaque arc :", arc_sources_targets)


    network.from_pyg_data(pyg_data)
    
    print("Graph loaded from transport_network.pth")
    visualize_network(network)
