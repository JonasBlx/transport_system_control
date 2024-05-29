import torch
from vehicle import Vehicle

class Node:
    def __init__(self, node_id, node_type, coordinates, capacity, vehicles, staff, service_hours, demand):
        """
        Initialize a node in the transportation network.
        
        Args:
            node_id (int): Unique identifier for the node.
            node_type (torch.Tensor): One-hot encoded tensor indicating types of the node (e.g., [bus_stop, railway_station, seaport, airport, hub]).
            coordinates (torch.Tensor): Tensor with [latitude, longitude].
            capacity (int): Capacity for handling passengers simultaneously.
            vehicles (list): List of Vehicle objects available at the node.
            staff (int): Number of staff available at the node.
            service_hours (torch.Tensor): Tensor with [opening_hour, closing_hour].
            demand (int): Current demand at the node.
        """
        self.node_id = node_id
        self.node_type = node_type
        self.coordinates = coordinates
        self.capacity = capacity
        self.vehicles = vehicles
        self.staff = staff
        self.service_hours = service_hours
        self.demand = demand

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle_id):
        self.vehicles = [v for v in self.vehicles if v.vehicle_id != vehicle_id]

    def get_id(self):
        return self.node_id

    def get_coordinates(self):
        return self.coordinates.tolist()

    def get_capacity(self):
        return self.capacity

    def get_vehicles(self):
        return self.vehicles

    def get_staff(self):
        return self.staff

    def get_service_hours(self):
        return self.service_hours.tolist()

    def get_demand(self):
        return self.demand

    def set_capacity(self, new_capacity):
        self.capacity = new_capacity

    def update_resources(self, resource_type, amount):
        if resource_type == 'vehicles':
            self.vehicles = amount
        elif resource_type == 'staff':
            self.staff = amount
        else:
            raise ValueError(f"Resource type {resource_type} not found in resources.")

    def update_demand(self, new_demand):
        self.demand = new_demand

    def is_operational(self, current_hour):
        if self.service_hours[0] == 0 and self.service_hours[1] == 0:
            return True
        return self.service_hours[0] <= current_hour < self.service_hours[1]

    def to_tensor(self):
        main_attributes_tensor = torch.tensor([
            self.node_id, self.capacity, len(self.vehicles), self.staff, self.demand
        ], dtype=torch.float)
        vehicle_tensors = torch.stack([v.to_tensor() for v in self.vehicles]) if self.vehicles else torch.empty((0,))
        return torch.cat((main_attributes_tensor, self.node_type, self.coordinates, self.service_hours)), vehicle_tensors

    def __repr__(self):
        return (f"Node(id={self.node_id}, type={self.node_type.tolist()}, coordinates={self.coordinates.tolist()}, "
                f"capacity={self.capacity}, vehicles={[v.vehicle_id for v in self.vehicles]}, staff={self.staff}, "
                f"service_hours={self.service_hours.tolist()}, demand={self.demand})")

# Exemple d'utilisation
if __name__ == "__main__":
    node = Node(
        node_id=1,
        node_type=torch.tensor([1, 0, 0, 0, 0]),  # One-hot encoded: [bus_stop, railway_station, seaport, airport, hub]
        coordinates=torch.tensor([48.8566, 2.3522]),  # Latitude and Longitude
        capacity=100,
        vehicles=[],
        staff=2,
        service_hours=torch.tensor([6.0, 22.0]),  # Opening hour: 6, Closing hour: 22
        demand=50  # Current demand
    )
    vehicle = Vehicle(
        vehicle_id=1,
        in_service=1,  # 1 for True (in service)
        vehicle_type=torch.tensor([1, 0, 0, 0]),  # One-hot encoded: [Truck, Train, Boat, Plane]
        is_node=1,  # 1 for node
        location_id=1,
        next_departure=2,
        capacity=100,
        capacity_left=50,
        service_hours=torch.tensor([6.0, 22.0])  # Opening hour: 6, Closing hour: 22
    )
    node.add_vehicle(vehicle)
    node_tensor, vehicles_tensor = node.to_tensor()
    print(node)
    print(node_tensor)
    print(vehicles_tensor)
