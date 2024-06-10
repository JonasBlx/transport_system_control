import torch
import pandas as pd
import sys
sys.path.append("../environment/")

from environment import Environment

def display_node_and_edge(pyg_filepath, node_size_csv, arc_size_csv):
    # Load the PyTorch Geometric data
    pyg_data = torch.load(pyg_filepath)
    
    # Load the sizes DataFrames
    node_sizes_df = pd.read_csv(node_size_csv)
    arc_sizes_df = pd.read_csv(arc_size_csv)
    
    # Create an environment and load the data
    network = Environment()
    network.from_pyg_data(pyg_data, node_sizes_df, arc_sizes_df)
    
    # Display the first node attributes
    if len(network.nodes) > 0:
        print("First Node Attributes:")
        first_node = list(network.nodes.values())[0]
        print(f"Node ID: {first_node.node_id}")
        print(f"Node Type: {first_node.node_type}")
        print(f"Coordinates: {first_node.coordinates}")
        print(f"Capacity: {first_node.capacity}")
        print(f"Number of Vehicles: {len(first_node.vehicles)}")
        print(f"Staff: {first_node.staff}")
        print(f"Service Hours: {first_node.service_hours}")
        print(f"Demand: {first_node.demand}")
    else:
        print("No nodes found in the data.")
    
    # Display the first edge attributes
    if len(network.arcs) > 0:
        print("\nFirst Edge Attributes:")
        first_arc = list(network.arcs.values())[0][0]
        source = list(network.arcs.values())[0][1]
        target = list(network.arcs.values())[0][2]
        print(f"Edge ID: {first_arc.arc_id}")
        print(f"Edge from Node {source} to Node {target}")
        print(f"Arc Type: {first_arc.arc_type}")
        print(f"Length: {first_arc.length}")
        print(f"Travel Time: {first_arc.travel_time}")
        print(f"Capacity: {first_arc.capacity}")
        print(f"Traffic Condition: {first_arc.traffic_condition}")
        print(f"Safety: {first_arc.safety}")
        print(f"Usage Cost: {first_arc.usage_cost}")
        print(f"Open: {first_arc.open}")
    else:
        print("No edges found in the data.")

if __name__ == "__main__":
    pyg_filepath = "../../data/generated/environment.pth"
    node_size_csv = "../../data/generated/node_sizes.csv"
    arc_size_csv = "../../data/generated/arc_sizes.csv"
    display_node_and_edge(pyg_filepath, node_size_csv, arc_size_csv)
