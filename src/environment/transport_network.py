import sys
sys.path.append("../../")

import pandas as pd
import torch
from torch_geometric.data import Data
from torch_geometric.utils import to_networkx
from src.environment.nodes import Node
from src.environment.arcs import Arc

class TransportNetwork:
    def __init__(self):
        self.nodes = {}
        self.arcs = {}

    def add_node(self, node):
        if node.node_id in self.nodes:
            raise ValueError(f"Node with ID {node.node_id} already exists.")
        self.nodes[node.node_id] = node

    def add_arc(self, arc, source, target):
        if source not in self.nodes or target not in self.nodes:
            print(f"Source nodes: {self.nodes}")
            print(f"Target nodes: {self.nodes}")
            print(f"Invalid arc from {source} to {target}")
            raise ValueError(f"Source or target node does not exist.aaaaaaaaaaaaaaaa")
        if arc.arc_id in self.arcs:
            raise ValueError(f"Arc with ID {arc.arc_id} already exists.")
        if source not in self.nodes or target not in self.nodes:
            raise ValueError(f"Source or target node does not exist.")
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
            node_features.append([
                node.bus_stop, node.railway_station, node.seaport, node.airport, node.hub,
                node.latitude, node.longitude, node.capacity, node.vehicles, node.staff,
                node.opening_hours, node.closing_hours
            ])  # Add more features as needed

        for arc_id, (arc, source, target) in self.arcs.items():
            if source not in self.nodes or target not in self.nodes:
                raise ValueError(f"Source or target node does not exist.")
            
            edge_index.append([node_index[source], node_index[target]])
            edge_attr.append([
                arc.road, arc.railway, arc.canal, arc.maritime, arc.air_route,
                arc.length, arc.travel_time, arc.capacity, arc.traffic_condition,
                arc.safety, arc.usage_cost, arc.open
            ])  # Add more attributes as needed

        x = torch.tensor(node_features, dtype=torch.float)
        edge_index = torch.tensor(edge_index, dtype=torch.long).t().contiguous()
        edge_attr = torch.tensor(edge_attr, dtype=torch.float)

        return Data(x=x, edge_index=edge_index, edge_attr=edge_attr)

    def from_pyg_data(self, data):
        # Clear existing nodes and arcs
        self.nodes.clear()
        self.arcs.clear()

        node_features = data.x.tolist()
        edge_index = data.edge_index.t().tolist()
        edge_attr = data.edge_attr.tolist()

        for i, features in enumerate(node_features):
            node = Node(
                node_id=i,
                bus_stop=features[0],
                railway_station=features[1],
                seaport=features[2],
                airport=features[3],
                hub=features[4],
                latitude=features[5],
                longitude=features[6],
                capacity=features[7],
                vehicles=features[8],
                staff=features[9],
                opening_hours=features[10],
                closing_hours=features[11]
            )
            self.add_node(node)

        for i, (source, target) in enumerate(edge_index):
            arc = Arc(
                arc_id=i,
                road=edge_attr[i][0],
                railway=edge_attr[i][1],
                canal=edge_attr[i][2],
                maritime=edge_attr[i][3],
                air_route=edge_attr[i][4],
                length=edge_attr[i][5],
                travel_time=edge_attr[i][6],
                capacity=edge_attr[i][7],
                traffic_condition=edge_attr[i][8],
                safety=edge_attr[i][9],
                usage_cost=edge_attr[i][10],
                open=edge_attr[i][11]
            )
            self.add_arc(arc, source, target)

    def get_state(self):
        state = {
            "nodes": {node_id: node.__dict__ for node_id, node in self.nodes.items()},
            "arcs": {arc_id: arc[0].__dict__ for arc_id, arc in self.arcs.items()}
        }
        return state

    def apply_action(self, action):
        action_type = action.get("type")
        
        if action_type == "update_node_capacity":
            node_id = action.get("node_id")
            new_capacity = action.get("new_capacity")
            if node_id in self.nodes:
                self.nodes[node_id].set_capacity(new_capacity)
            else:
                raise ValueError(f"Node with ID {node_id} does not exist.")
        
        elif action_type == "update_arc_dynamic_data":
            arc_id = action.get("arc_id")
            key = action.get("key")
            value = action.get("value")
            if arc_id in self.arcs:
                self.arcs[arc_id][0].update_dynamic_data(key, value)
            else:
                raise ValueError(f"Arc with ID {arc_id} does not exist.")
        
        else:
            raise ValueError(f"Unknown action type: {action_type}")

    def __repr__(self):
        return f"TransportNetwork(nodes={list(self.nodes.keys())}, arcs={list(self.arcs.keys())})"

def load_network_from_csv(node_file_path, arc_file_path):
    network = TransportNetwork()
    
    # Load nodes
    df_nodes = pd.read_csv(node_file_path)
    for _, row in df_nodes.iterrows():
        node = Node(
            node_id=row["node_id"],
            bus_stop=row["bus_stop"],
            railway_station=row["railway_station"],
            seaport=row["seaport"],
            airport=row["airport"],
            hub=row["hub"],
            latitude=row["latitude"],
            longitude=row["longitude"],
            capacity=row["capacity"],
            vehicles=row["vehicles"],
            staff=row["staff"],
            opening_hours=row["opening_hours"],
            closing_hours=row["closing_hours"]
        )
        network.add_node(node)
    
    # Load arcs
    df_arcs = pd.read_csv(arc_file_path)
    for _, row in df_arcs.iterrows():
        arc = Arc(
            arc_id=row["arc_id"],
            road=row["road"],
            railway=row["railway"],
            canal=row["canal"],
            maritime=row["maritime"],
            air_route=row["air_route"],
            length=row["length"],
            travel_time=row["travel_time"],
            capacity=row["capacity"],
            traffic_condition=row["traffic_condition"],
            safety=row["safety"],
            usage_cost=row["usage_cost"],
            open=row["open"]
        )
        network.add_arc(arc, row["source"], row["target"])
    
    return network

# Example usage
if __name__ == "__main__":
    node_file_path = "../../data/generated/nodes_example_1.csv"
    arc_file_path = "../../data/generated/arcs_example_1.csv"
    
    network = load_network_from_csv(node_file_path, arc_file_path)
    pyg_data = network.to_pyg_data()
    torch.save(pyg_data, "../../data/generated/transport_network.pth")
    print("Graph saved to transport_network.pth")
