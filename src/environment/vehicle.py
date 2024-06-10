import torch

class Vehicle:
    def __init__(self, id, in_service, type, is_node, location_id, start, capacity, capacity_left, service_hours, circuit):
        """
        Initialize a vehicle in the transportation network.

        Args:
            id (int): Unique identifier for the vehicle.
            in_service (int): 0 or 1 indicating if the vehicle is in service.
            type (torch.Tensor): One-hot encoded tensor indicating type of the vehicle (e.g., [1, 0, 0, 0] for Truck).
            is_node (int): 0 for an arc or 1 for a node.
            location_id (int): ID related to either a node or an arc.
            start (int): 1 if the vehicle is starting a trip, 0 otherwise.
            capacity (int): Capacity of the vehicle (number of passengers or amount of freight).
            capacity_left (int): Remaining capacity of the vehicle.
            service_hours (torch.Tensor): Tensor [opening hour, closing hour] representing operational hours.
            circuit (list): List of node IDs representing the path for the next trip/current trip.
        """
        self.id = id
        self.in_service = in_service
        self.type = type
        self.is_node = is_node
        self.location_id = location_id
        self.start = start
        self.capacity = capacity
        self.capacity_left = capacity_left
        self.service_hours = service_hours
        self.circuit = circuit

    def to_tensor(self):
        main_attributes_tensor = torch.tensor([
            self.id, self.in_service, self.is_node, self.location_id,
            self.start, self.capacity, self.capacity_left
        ], dtype=torch.float)
        type_tensor = self.type
        service_hours_tensor = self.service_hours
        circuit_tensor = torch.tensor(self.circuit, dtype=torch.float) if self.circuit else torch.empty((0,))
        return torch.cat((main_attributes_tensor, type_tensor, service_hours_tensor, circuit_tensor))

    def __repr__(self):
        return (f"Vehicle(id={self.id}, in_service={self.in_service}, type={self.type.tolist()}, "
                f"is_node={self.is_node}, location_id={self.location_id}, start={self.start}, "
                f"capacity={self.capacity}, capacity_left={self.capacity_left}, service_hours={self.service_hours.tolist()}, "
                f"circuit={self.circuit})")

# Exemple d'utilisation
if __name__ == "__main__":
    vehicle = Vehicle(
        id=1,
        in_service=1,  # 1 for True (in service)
        type=torch.tensor([1, 0, 0, 0]),  # One-hot encoded: [Truck, Train, Boat, Plane]
        is_node=1,  # 1 for node
        location_id=42,
        start=1,  # 1 if the vehicle is starting a trip
        capacity=100,
        capacity_left=50,
        service_hours=torch.tensor([6.0, 22.0]),  # Opening hour: 6, Closing hour: 22
        circuit=[42, 43, 44]  # Example path for the next trip
    )
    vehicle_tensor = vehicle.to_tensor()
    print(vehicle)
    print(vehicle_tensor)
