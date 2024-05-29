import torch


def display_node_and_edge(filepath):
    # Load the PyTorch Geometric data
    pyg_data = torch.load(filepath)
    
    # Display the first node features
    if pyg_data.x.size(0) > 0:
        print("First Node Features:")
        first_node_features = pyg_data.x[0]
        print(first_node_features)
        print("\nParsed Node Features:")
        print(f"Node Type: {first_node_features[:5]}")
        print(f"Coordinates: {first_node_features[5:7]}")
        print(f"Capacity: {first_node_features[7].item()}")
        #print(f"Number of Vehicles: {first_node_features[8].item()}")
        print(f"Staff: {first_node_features[8].item()}")
        print(f"Service Hours: {first_node_features[9:11]}")
        print(f"Demand: {first_node_features[11].item()}")
    else:
        print("No nodes found in the data.")
    
    # Display the first edge attributes
    if pyg_data.edge_index.size(1) > 0:
        print("\nFirst Edge Attributes:")
        first_edge_index = pyg_data.edge_index[:, 0]
        first_edge_attr = pyg_data.edge_attr[0]
        print(f"Edge from Node {first_edge_index[0].item()} to Node {first_edge_index[1].item()}")
        print(first_edge_attr)
        print("\nParsed Edge Attributes:")
        print(f"Arc Type: {first_edge_attr[:5]}")
        print(f"Length: {first_edge_attr[5].item()}")
        print(f"Travel Time: {first_edge_attr[6].item()}")
        print(f"Capacity: {first_edge_attr[7].item()}")
        print(f"Traffic Condition: {first_edge_attr[8].item()}")
        print(f"Safety: {first_edge_attr[9].item()}")
        print(f"Usage Cost: {first_edge_attr[10].item()}")
        print(f"Open: {first_edge_attr[11].item()}")
    else:
        print("No edges found in the data.")

if __name__ == "__main__":
    filepath = "../../data/generated/transport_network.pth"
    display_node_and_edge(filepath)
