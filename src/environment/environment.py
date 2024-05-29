import sys
sys.path.append("../../")

import numpy as np
import pandas as pd
import torch
import ast
from torch_geometric.data import Data
from torch_geometric.utils import to_networkx
from nodes import Node
from arcs import Arc
from vehicle import Vehicle

class Environment:
    def __init__(self):
        self.nodes = {}
        self.arcs = {}
        self.vehicles = {}
        self.current_time = 0

    def add_node(self, node):
        if node.node_id in self.nodes:
            raise ValueError(f"Node with ID {node.node_id} already exists.")
        self.nodes[node.node_id] = node

    def add_arc(self, arc, source, target):
        if source not in self.nodes or target not in self.nodes:
            raise ValueError(f"Source or target node does not exist.")
        if arc.arc_id in self.arcs:
            raise ValueError(f"Arc with ID {arc.arc_id} already exists.")
        self.arcs[arc.arc_id] = (arc, source, target)

    def get_node(self, node_id):
        return self.nodes.get(node_id, None)

    def get_arc(self, arc_id):
        return self.arcs.get(arc_id, None)

    def to_pyg_data(self):
        node_features = []
        edge_index = []
        edge_attr = []

        node_index = {node_id: i for i, node_id in enumerate(self.nodes)}

        for node_id, node in self.nodes.items():
            try:
                node_features.append(torch.cat([
                    node.node_type,
                    node.coordinates,
                    torch.tensor([node.capacity], dtype=torch.float),
                    #torch.tensor([len(node.vehicles)], dtype=torch.float),
                    torch.tensor([node.staff], dtype=torch.float),
                    node.service_hours,
                    torch.tensor([node.demand], dtype=torch.float)
                ]))
            except TypeError as e:
                print(f"Error processing node {node_id}: {e}")
                print(f"node_type: {node.node_type}, coordinates: {node.coordinates}, capacity: {node.capacity}, vehicles: {len(node.vehicles)}, staff: {node.staff}, service_hours: {node.service_hours}, demand: {node.demand}")
                raise e

        for arc_id, (arc, source, target) in self.arcs.items():
            if source not in self.nodes or target not in self.nodes:
                raise ValueError(f"Source or target node does not exist.")
            
            edge_index.append([node_index[source], node_index[target]])
            edge_attr.append(torch.cat([
                arc.arc_type, 
                torch.tensor([arc.length], dtype=torch.float), 
                torch.tensor([arc.travel_time], dtype=torch.float), 
                torch.tensor([arc.capacity], dtype=torch.float), 
                torch.tensor([arc.traffic_condition], dtype=torch.float),
                torch.tensor([arc.safety], dtype=torch.float), 
                torch.tensor([arc.usage_cost], dtype=torch.float), 
                #torch.tensor([arc.vehicle], dtype=torch.float),
                torch.tensor([arc.open], dtype=torch.float)
            ]))

        x = torch.stack(node_features)
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        edge_attr = torch.stack(edge_attr)

        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)

    def from_pyg_data(self, data): # This method does not scale correctly 
        #and must be modified if the number of columns in features is changed.
        # Clear existing nodes and arcs
        self.nodes.clear()
        self.arcs.clear()

        node_features = data.x.tolist()
        edge_index = data.edge_index.t().tolist()
        edge_attr = data.edge_attr.tolist()

        for i, features in enumerate(node_features):
            node_type = features[:5]  # Node type as a one-hot encoded tensor
            coordinates = features[5:7]  # Coordinates as [latitude, longitude]
            capacity = features[7]  # Capacity
            #vehicles = features[8]  # Number of vehicles
            staff = features[8]  # Staff
            service_hours = features[9:11]  # Service hours as [opening_hour, closing_hour]
            demand = features[11]  # Demand

            node = Node(
                node_id=i,
                node_type=torch.tensor(node_type, dtype=torch.float),
                coordinates=torch.tensor(coordinates, dtype=torch.float),
                capacity=int(capacity),
                vehicles=[],  # Initialize empty, to be updated later
                staff=int(staff),
                service_hours=torch.tensor(service_hours, dtype=torch.float),
                demand=int(demand)
            )
            self.add_node(node)

        for i, (source, target) in enumerate(edge_index):
            arc_type = edge_attr[i][:5]  # Arc type as a one-hot encoded tensor
            length = edge_attr[i][5]  # Length
            travel_time = edge_attr[i][6]  # Travel time
            capacity = edge_attr[i][7]  # Capacity
            traffic_condition = edge_attr[i][8]  # Traffic condition
            safety = edge_attr[i][9]  # Safety
            usage_cost = edge_attr[i][10]  # Usage cost
            open_status = edge_attr[i][11]  # Open status

            arc = Arc(
                arc_id=i,
                arc_type=torch.tensor(arc_type, dtype=torch.float),
                length=float(length),
                travel_time=float(travel_time),
                capacity=int(capacity),
                traffic_condition=int(traffic_condition),
                safety=int(safety),
                usage_cost=float(usage_cost),
                open=int(open_status),
                source=source,
                target=target,
                vehicles=[]  # Initialize empty, to be updated later
            )
            self.add_arc(arc, source, target)


    def get_state(self):
        state = {
            "nodes": {node_id: node.__dict__ for node_id, node in self.nodes.items()},
            "arcs": {arc_id: arc[0].__dict__ for arc_id, arc in self.arcs.items()}
        }
        return state
    
    def step(self, schedule):
        # Apply the schedule
        for event in schedule:
            self.apply_event(event)
        
        # Update the state of vehicles, nodes, and arcs, including demand
        self.update_state()
        
        # Advance time
        self.current_time += 1
        
        # Calculate the reward
        reward = self.calculate_reward()
        
        # Check if the episode is done (here, the episode always continues)
        done = False
        
        # Get the new state
        new_state = self.get_state()
        
        return new_state, reward, done

    def calculate_reward(self):
        # Calculate the total unmet demand
        total_unsatisfied_demand = sum(node.demand for node in self.nodes.values())
        
        # Calculate the standard deviation of demands across nodes
        demands = [node.demand for node in self.nodes.values()]
        demand_std_dev = np.std(demands)
        
        # Calculate the combined reward
        reward = - (total_unsatisfied_demand + 0.1 * demand_std_dev)
        
        return reward
    
    def update_state(self):
        # Update the state of vehicles (positions, statuses, capacities)
        for vehicle in self.vehicles.values():
            # Logic to update each vehicle
            pass

        # Update the state of nodes (capacities, demands, etc.)
        for node in self.nodes.values():
            # Logic to update each node
            self.update_demand(node)
            pass

        # Update the state of arcs (capacities, traffic, etc.)
        for arc in self.arcs.values():
            # Logic to update each arc
            pass
    
    def update_demand(self, node):
        # Logic to update the demand of a node
        # Increase demand according to the defined distribution
        node.demand += self.calculate_new_demand(node)

    def __repr__(self):
        return f"Environment(nodes={list(self.nodes.keys())}, arcs={list(self.arcs.keys())})"


def load_network_from_csv(node_file_path, arc_file_path):
    environment = Environment()
    
    # Load nodes
    df_nodes = pd.read_csv(node_file_path)
    for _, row in df_nodes.iterrows():
        node = Node(
            node_id=row["node_id"],
            node_type=torch.tensor(ast.literal_eval(row["node_type"]), dtype=torch.float),
            coordinates=torch.tensor(ast.literal_eval(row["coordinates"]), dtype=torch.float),
            capacity=row["capacity"],
            vehicles=[],  # Initialize empty, to be updated later
            staff=row["staff"],
            service_hours=torch.tensor(ast.literal_eval(row["service_hours"]), dtype=torch.float),
            demand=row["demand"]
        )
        environment.add_node(node)
    
    # Load arcs
    df_arcs = pd.read_csv(arc_file_path)
    for _, row in df_arcs.iterrows():
        arc = Arc(
            arc_id=row["arc_id"],
            arc_type=torch.tensor(ast.literal_eval(row["arc_type"]), dtype=torch.float),
            length=row["length"],
            travel_time=row["travel_time"],
            capacity=row["capacity"],
            traffic_condition=row["traffic_condition"],
            safety=row["safety"],
            usage_cost=row["usage_cost"],
            open=row["open"],
            source=row["source"],
            target=row["target"],
            vehicles=[]  # Initialize empty, to be updated later
        )
        environment.add_arc(arc, row["source"], row["target"])
    
    return environment

# Example usage
if __name__ == "__main__":
    node_file_path = "../../data/generated/nodes_example_1.csv"
    arc_file_path = "../../data/generated/arcs_example_1.csv"
    
    environment = load_network_from_csv(node_file_path, arc_file_path)
    pyg_data = environment.to_pyg_data()
    torch.save(pyg_data, "../../data/generated/environment.pth")
    print("Graph saved to environment.pth")