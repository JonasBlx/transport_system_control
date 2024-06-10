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
from update import update_demand

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
        node_sizes = []
        arc_sizes = []

        node_index = {node_id: i for i, node_id in enumerate(self.nodes)}

        for node_id, node in self.nodes.items():
            node_attr = [
                node.node_type,
                node.coordinates,
                torch.tensor([node.capacity], dtype=torch.float),
                torch.tensor([node.staff], dtype=torch.float),
                node.service_hours,
                torch.tensor([node.demand], dtype=torch.float)
            ]
            node_sizes.append([node_id] + [len(attr) for attr in node_attr])
            node_features.append(torch.cat(node_attr))

        for arc_id, (arc, source, target) in self.arcs.items():
            if source not in self.nodes or target not in self.nodes:
                raise ValueError(f"Source or target node does not exist.")
            
            arc_attr = [
                arc.arc_type, 
                torch.tensor([arc.length], dtype=torch.float), 
                torch.tensor([arc.travel_time], dtype=torch.float), 
                torch.tensor([arc.capacity], dtype=torch.float), 
                torch.tensor([arc.traffic_condition], dtype=torch.float),
                torch.tensor([arc.safety], dtype=torch.float), 
                torch.tensor([arc.usage_cost], dtype=torch.float), 
                torch.tensor([arc.open], dtype=torch.float)
            ]
            arc_sizes.append([arc_id] + [len(attr) for attr in arc_attr])
            edge_index.append([node_index[source], node_index[target]])
            edge_attr.append(torch.cat(arc_attr))

        x = torch.stack(node_features)
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        edge_attr = torch.stack(edge_attr)

        node_sizes_df = pd.DataFrame(node_sizes, columns=['node_id', 'node_type_size', 'coordinates_size', 'capacity_size', 'staff_size', 'service_hours_size', 'demand_size'])
        arc_sizes_df = pd.DataFrame(arc_sizes, columns=['arc_id', 'arc_type_size', 'length_size', 'travel_time_size', 'capacity_size', 'traffic_condition_size', 'safety_size', 'usage_cost_size', 'open_size'])

        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr), node_sizes_df, arc_sizes_df

    def from_pyg_data(self, data, node_sizes_df, arc_sizes_df):
        self.nodes.clear()
        self.arcs.clear()

        node_features = data.x.tolist()
        edge_index = data.edge_index.t().tolist()
        edge_attr = data.edge_attr.tolist()

        node_id_to_idx = {row['node_id']: idx for idx, row in node_sizes_df.iterrows()}
        arc_id_to_idx = {row['arc_id']: idx for idx, row in arc_sizes_df.iterrows()}

        # Add nodes
        for node_id, idx in node_id_to_idx.items():
            node_sizes = node_sizes_df.iloc[idx]
            start = 0
            node_type = node_features[idx][start:start + node_sizes['node_type_size']]
            start += node_sizes['node_type_size']
            coordinates = node_features[idx][start:start + node_sizes['coordinates_size']]
            start += node_sizes['coordinates_size']
            capacity = node_features[idx][start:start + node_sizes['capacity_size']][0]
            start += node_sizes['capacity_size']
            staff = node_features[idx][start:start + node_sizes['staff_size']][0]
            start += node_sizes['staff_size']
            service_hours = node_features[idx][start:start + node_sizes['service_hours_size']]
            start += node_sizes['service_hours_size']
            demand = node_features[idx][start:start + node_sizes['demand_size']][0]

            node = Node(
                node_id=node_id,
                node_type=torch.tensor(node_type, dtype=torch.float),
                coordinates=torch.tensor(coordinates, dtype=torch.float),
                capacity=int(capacity),
                vehicles=[],
                staff=int(staff),
                service_hours=torch.tensor(service_hours, dtype=torch.float),
                demand=int(demand)
            )
            self.add_node(node)

        print("nodes are : ---")
        print(self.nodes.keys())
        print("---")

        # Create a mapping from index to node_id
        idx_to_node_id = {v: k for k, v in node_id_to_idx.items()}

        # Add arcs
        for arc_id, idx in arc_id_to_idx.items():
            arc_sizes = arc_sizes_df.iloc[idx]
            start = 0
            arc_type = edge_attr[idx][start:start + arc_sizes['arc_type_size']]
            start += arc_sizes['arc_type_size']
            length = edge_attr[idx][start:start + arc_sizes['length_size']][0]
            start += arc_sizes['length_size']
            travel_time = edge_attr[idx][start:start + arc_sizes['travel_time_size']][0]
            start += arc_sizes['travel_time_size']
            capacity = edge_attr[idx][start:start + arc_sizes['capacity_size']][0]
            start += arc_sizes['capacity_size']
            traffic_condition = edge_attr[idx][start:start + arc_sizes['traffic_condition_size']][0]
            start += arc_sizes['traffic_condition_size']
            safety = edge_attr[idx][start:start + arc_sizes['safety_size']][0]
            start += arc_sizes['safety_size']
            usage_cost = edge_attr[idx][start:start + arc_sizes['usage_cost_size']][0]
            start += arc_sizes['usage_cost_size']
            open_status = edge_attr[idx][start:start + arc_sizes['open_size']][0]

            source_idx = edge_index[idx][0]
            target_idx = edge_index[idx][1]

            source = idx_to_node_id[source_idx]
            target = idx_to_node_id[target_idx]

            # Ensure the source and target nodes exist
            if source not in self.nodes or target not in self.nodes:
                raise ValueError(f"Source or target node does not exist for arc {arc_id} (source: {source}, target: {target})")

            arc = Arc(
                arc_id=arc_id,
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
                vehicles=[]
            )
            self.add_arc(arc, source, target)


    def get_state(self):
        state = {
            "nodes": {node_id: node.__dict__ for node_id, node in self.nodes.items()},
            "arcs": {arc_id: arc[0].__dict__ for arc_id, arc in self.arcs.items()}
        }
        return state
    
    def step(self, schedule):
        for event in schedule:
            self.apply_event(event)
        
        self.update_state()
        self.current_time += 1
        reward = self.calculate_reward()
        done = False
        new_state = self.get_state()
        
        return new_state, reward, done
    
    def apply_event(self, event):
        pass

    def calculate_reward(self):
        total_unsatisfied_demand = sum(node.demand for node in self.nodes.values())
        demands = [node.demand for node in self.nodes.values()]
        demand_std_dev = np.std(demands)
        reward = - (total_unsatisfied_demand + 0.1 * demand_std_dev)
        return reward
    
    def update_state(self):
        for vehicle in self.vehicles.values():
            self.vehicle_step(vehicle)

        for node in self.nodes.values():
            self.update_demand(node)
            pass

        for arc in self.arcs.values():
            pass
    
    def update_demand(self, node):
        node.demand += update_demand(self.current_time)

    def vehicle_step(self, vehicle):
        pass

    def __repr__(self):
        return f"Environment(nodes={list(self.nodes.keys())}, arcs={list(self.arcs.keys())})"


def load_network_from_csv(node_file_path, arc_file_path):
    environment = Environment()
    
    df_nodes = pd.read_csv(node_file_path)
    for _, row in df_nodes.iterrows():
        node = Node(
            node_id=row["node_id"],
            node_type=torch.tensor(ast.literal_eval(row["node_type"]), dtype=torch.float),
            coordinates=torch.tensor(ast.literal_eval(row["coordinates"]), dtype=torch.float),
            capacity=row["capacity"],
            vehicles=[],
            staff=row["staff"],
            service_hours=torch.tensor(ast.literal_eval(row["service_hours"]), dtype=torch.float),
            demand=row["demand"]
        )
        environment.add_node(node)
    
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
            vehicles=[]
        )
        environment.add_arc(arc, row["source"], row["target"])
    
    return environment

# Example usage
if __name__ == "__main__":
    node_file_path = "../../data/generated/nodes_example_1.csv"
    arc_file_path = "../../data/generated/arcs_example_1.csv"
    
    environment = load_network_from_csv(node_file_path, arc_file_path)
    pyg_data, node_sizes_df, arc_sizes_df = environment.to_pyg_data()
    torch.save(pyg_data, "../../data/generated/environment.pth")
    node_sizes_df.to_csv("../../data/generated/node_sizes.csv", index=False)
    arc_sizes_df.to_csv("../../data/generated/arc_sizes.csv", index=False)
    print("Graph and sizes saved to environment.pth, node_sizes.csv, and arc_sizes.csv")