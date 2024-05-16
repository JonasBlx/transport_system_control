import pandas as pd
import numpy as np

# Assuming the CSV 'arcs.csv' is properly formatted and includes columns 'Node1' and 'Node2'
df = pd.read_csv('raw_data/arcs.csv')

# Find all unique nodes
nodes = np.unique(df[['Node1', 'Node2']].values)

# Create an adjacency matrix of zeros
adj_matrix = np.zeros((len(nodes), len(nodes)), dtype=int)

# Map node IDs to matrix indices
node_index = {node: idx for idx, node in enumerate(nodes)}

# Populate the adjacency matrix for an undirected graph
for _, row in df.iterrows():
    src_idx = node_index[row['Node1']]
    tgt_idx = node_index[row['Node2']]
    # Set both matrix entries to indicate an undirected edge
    adj_matrix[src_idx][tgt_idx] = 1
    adj_matrix[tgt_idx][src_idx] = 1  # This line ensures the matrix is symmetric

# Display the adjacency matrix
print(adj_matrix)



df['ID'] = df.apply(lambda row: (row['Node1'], row['Node2']) 
                    if adj_matrix[node_index[row['Node1']], node_index[row['Node2']]] == 1 
                    else None, axis=1)

# Drop the "Node1" and "Node2" columns from the dataframe
df = df.drop(columns=["Node1", "Node2"])

print(df)

df.to_csv('structured_data/structured_arcs.csv', index=False)