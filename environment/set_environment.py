import pandas as pd
import numpy as np
import torch
from torch_geometric.data import Data

# Load node and arc data
node_df = pd.read_csv('processed_data/processed_nodes.csv')
arc_df = pd.read_csv('processed_data/processed_arcs.csv')

# Node features (assuming numerical data is already suitable for use as features)
node_features = node_df[['Capacity', 'Latitude', 'Longitude', 'Vehicle_Availability', 'Driver_Availability', 'Opening_Hours', 'Closing_Hours', 'Airport', 'Bus Stop', 'Multimodal Hub', 'Railway Station', 'Seaport']].to_numpy()
node_features_tensor = torch.tensor(node_features, dtype=torch.float)

# Prepare edge index for non-oriented graph (bidirectional edges)
arc_df['Parsed_IDs'] = arc_df['ID'].apply(lambda x: eval(x))
edge_start = arc_df['Parsed_IDs'].apply(lambda x: x[0] - 1).to_numpy()
edge_end = arc_df['Parsed_IDs'].apply(lambda x: x[1] - 1).to_numpy()

# Convert to numpy array before creating the tensor
edge_index = torch.tensor(np.array([edge_start, edge_end]), dtype=torch.long)

# Add reverse direction
edge_index = torch.cat([edge_index, edge_index[[1, 0], :]], dim=1)

# Edge features
edge_features = arc_df[['Length_km', 'Travel_Time', 'Traffic_Conditions', 'Infrastructure_Quality', 'Safety', 'Dynamic_Data', 'Vehicle_Capacity', 'Passenger_Capacity', 'Cost', 'Maintenance', 'Air_Route', 'Maritime_Route', 'Railway', 'Road']].to_numpy()
edge_features_tensor = torch.tensor(edge_features, dtype=torch.float)

# Create graph data object
data = Data(x=node_features_tensor, edge_index=edge_index, edge_attr=edge_features_tensor)

# Optionally, if using only CPU (adjust according to your setup)
device = torch.device('cpu')
data = data.to(device)

print(data)


import networkx as nx
import matplotlib.pyplot as plt
from torch_geometric.utils import to_networkx

# Assuming 'data' is already created and contains your graph data
G = to_networkx(data, to_undirected=True)  # Convert to undirected graph if your graph is non-oriented

# Position nodes using the geographic coordinates (if applicable)
pos = {i: (data.x[i][1].item(), data.x[i][2].item()) for i in range(data.num_nodes)}

# Draw the graph
plt.figure(figsize=(10, 8))
nx.draw(G, pos, node_color='lightblue', with_labels=True, node_size=700)
nx.draw_networkx_edge_labels(G, pos, edge_labels={(i, j): f'{data.edge_attr[k][0].item()}km' for k, (i, j) in enumerate(G.edges())})
plt.title('Graph Representation of Nodes and Arcs')
plt.show()
