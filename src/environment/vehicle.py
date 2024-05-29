import torch

class Vehicle:
    def __init__(self, vehicle_id, in_service, vehicle_type, is_node, location_id, next_departure, capacity, capacity_left, service_hours):
        """
        Initialize a vehicle in the transportation network.

        Args:
            vehicle_id (int): Unique identifier for the vehicle.
            in_service (int): 0 or 1 indicating if the vehicle is in service.
            vehicle_type (torch.Tensor): One-hot encoded tensor indicating type of the vehicle (e.g., [1, 0, 0, 0] for Truck).
            is_node (int): 0 for an arc or 1 for a node.
            location_id (int): ID related to either a node or an arc.
            next_departure (float): Number of steps left before the next departure.
            capacity (int): Capacity of the vehicle (number of passengers or amount of freight).
            capacity_left (int): Remaining capacity of the vehicle.
            service_hours (torch.Tensor): Tensor [opening hour, closing hour] representing operational hours.
        """
        self.vehicle_id = vehicle_id
        self.in_service = in_service
        self.vehicle_type = vehicle_type
        self.is_node = is_node
        self.location_id = location_id
        self.next_departure = next_departure
        self.capacity = capacity
        self.capacity_left = capacity_left
        self.service_hours = service_hours

    def to_tensor(self):
        main_attributes_tensor = torch.tensor([
            self.vehicle_id, self.in_service, self.is_node, self.location_id,
            self.next_departure, self.capacity, self.capacity_left
        ], dtype=torch.float)
        vehicle_type_tensor = self.vehicle_type
        service_hours_tensor = self.service_hours
        return torch.cat((main_attributes_tensor, vehicle_type_tensor, service_hours_tensor))

    def __repr__(self):
        return (f"Vehicle(id={self.v1Aehicle_id}, in_service={self.in_service}, type={self.vehicle_type.tolist()}, "
                f"is_node={self.is_node}, location_id={self.location_id}, next_departure={self.next_departure}, "
                f"capacity={self.capacity}, capacity_left={self.capacity_left}, service_hours={self.service_hours.tolist()})")

# Exemple d'utilisation
if __name__ == "__main__":
    vehicle = Vehicle(
        vehicle_id=1,
        in_service=1,  # 1 for True (in service)
        vehicle_type=torch.tensor([1, 0, 0, 0]),  # One-hot encoded: [Truck, Train, Boat, Plane]
        is_node=1,  # 1 for node
        location_id=42,
        next_departure=3,  # Timestamp
        capacity=100,
        capacity_left=50,
        service_hours=torch.tensor([6.0, 22.0])  # Opening hour: 6, Closing hour: 22
    )
    vehicle_tensor = vehicle.to_tensor()
    print(vehicle)
    print(vehicle_tensor)
