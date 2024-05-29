import torch
from nodes import Node
from arcs import Arc
from environment import Environment, load_network_from_csv

def print_node_details(node):
    print(f"Node ID: {node.node_id}")
    print(f"Node Type: {node.node_type.tolist()}")
    print(f"Coordinates: {node.coordinates.tolist()}")
    print(f"Capacity: {node.capacity}")
    print(f"Number of Vehicles: {len(node.vehicles)}")
    print(f"Staff: {node.staff}")
    print(f"Service Hours: {node.service_hours.tolist()}")
    print(f"Demand: {node.demand}")
    print("Vehicles:")
    for vehicle in node.vehicles:
        print(f"  Vehicle ID: {vehicle.vehicle_id}")
        print(f"  In Service: {vehicle.in_service}")
        print(f"  Vehicle Type: {vehicle.vehicle_type.tolist()}")
        print(f"  Is Node: {vehicle.is_node}")
        print(f"  Location ID: {vehicle.location_id}")
        print(f"  Next Departure: {vehicle.next_departure}")
        print(f"  Capacity: {vehicle.capacity}")
        print(f"  Capacity Left: {vehicle.capacity_left}")
        print(f"  Service Hours: {vehicle.service_hours.tolist()}")

if __name__ == "__main__":
    node_file_path = "../../data/generated/nodes_example_1.csv"
    arc_file_path = "../../data/generated/arcs_example_1.csv"
    
    environment = load_network_from_csv(node_file_path, arc_file_path)
    
    # Assuming we want to print details of the node with ID 1
    node_id_to_print = 1
    node = environment.get_node(node_id_to_print)
    if node:
        print_node_details(node)
    else:
        print(f"Node with ID {node_id_to_print} not found.")
