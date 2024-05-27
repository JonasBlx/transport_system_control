import torch

class Node:
    def __init__(self, node_id, node_type, coordinates, capacity, vehicles, staff, service_hours):
        """
        Initialize a node in the transportation network.
        
        Args:
            node_id (int): Unique identifier for the node.
            node_type (torch.Tensor): One-hot encoded tensor indicating types of the node (e.g., [bus_stop, railway_station, seaport, airport, hub]).
            coordinates (torch.Tensor): Tensor with [latitude, longitude].
            capacity (int): Capacity for handling passengers simultaneously.
            vehicles (int): Number of vehicles available at the node.
            staff (int): Number of staff available at the node.
            service_hours (torch.Tensor): Tensor with [opening_hour, closing_hour].
        """
        self.node_id = node_id
        self.node_type = node_type
        self.coordinates = coordinates
        self.capacity = capacity
        self.vehicles = vehicles
        self.staff = staff
        self.service_hours = service_hours

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

    def set_capacity(self, new_capacity):
        self.capacity = new_capacity

    def update_resources(self, resource_type, amount):
        if resource_type == 'vehicles':
            self.vehicles = amount
        elif resource_type == 'staff':
            self.staff = amount
        else:
            raise ValueError(f"Resource type {resource_type} not found in resources.")

    def is_operational(self, current_hour):
        if self.service_hours[0] == 0 and self.service_hours[1] == 0:
            return True
        return self.service_hours[0] <= current_hour < self.service_hours[1]

    def to_tensor(self):
        main_attributes_tensor = torch.tensor([
            self.node_id, self.capacity, self.vehicles, self.staff
        ], dtype=torch.float)
        return torch.cat((main_attributes_tensor, self.node_type, self.coordinates, self.service_hours))

    def __repr__(self):
        return (f"Node(id={self.node_id}, type={self.node_type.tolist()}, coordinates={self.coordinates.tolist()}, "
                f"capacity={self.capacity}, vehicles={self.vehicles}, staff={self.staff}, "
                f"service_hours={self.service_hours.tolist()})")

# Exemple d'utilisation
if __name__ == "__main__":
    node = Node(
        node_id=1,
        node_type=torch.tensor([1, 0, 0, 0, 0]),  # One-hot encoded: [bus_stop, railway_station, seaport, airport, hub]
        coordinates=torch.tensor([48.8566, 2.3522]),  # Latitude and Longitude
        capacity=100,
        vehicles=5,
        staff=2,
        service_hours=torch.tensor([6.0, 22.0])  # Opening hour: 6, Closing hour: 22
    )
    node_tensor = node.to_tensor()
    print(node)
    print(node_tensor)
