import torch

class Arc:
    def __init__(self, arc_id, arc_type, length, travel_time, capacity, traffic_condition, safety, usage_cost, open, source, target, vehicles):
        """
        Initialize an arc in the transportation network.

        Args:
            arc_id (int): Unique identifier for the arc.
            arc_type (torch.Tensor): One-hot encoded tensor indicating types of the arc (e.g., [road, railway, canal, maritime, air_route]).
            length (float): Length of the arc in kilometers.
            travel_time (float): Average travel time in minutes.
            capacity (int): Maximum number of vehicles or passengers that can travel simultaneously.
            traffic_condition (int): Traffic condition (0 for poor, 1 for average, 2 for good).
            safety (int): Safety mark out of 10.
            usage_cost (float): Cost associated with using the arc (e.g., toll fees, maintenance costs).
            open (int): 1 if the arc is open, 0 if it's closed.
            source (int): ID of the source node.
            target (int): ID of the target node.
            vehicles (list): List of Vehicle objects currently on the arc.
        """
        self.arc_id = arc_id
        self.arc_type = arc_type
        self.length = length
        self.travel_time = travel_time
        self.capacity = capacity
        self.traffic_condition = traffic_condition
        self.safety = safety
        self.usage_cost = usage_cost
        self.open = open
        self.source = source
        self.target = target
        self.vehicles = vehicles

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle_id):
        self.vehicles = [v for v in self.vehicles if v.vehicle_id != vehicle_id]

    def get_id(self):
        return self.arc_id

    def get_length(self):
        return self.length

    def get_travel_time(self):
        return self.travel_time

    def get_capacity(self):
        return self.capacity

    def get_traffic_condition(self):
        return self.traffic_condition

    def get_safety(self):
        return self.safety

    def get_usage_cost(self):
        return self.usage_cost

    def get_open(self):
        return self.open

    def to_tensor(self):
        main_attributes_tensor = torch.tensor([
            self.arc_id, self.length, self.travel_time, self.capacity,
            self.traffic_condition, self.safety, self.usage_cost, self.open,
            self.source, self.target
        ], dtype=torch.float)
        vehicle_tensors = torch.stack([v.to_tensor() for v in self.vehicles]) if self.vehicles else torch.empty((0,))
        return torch.cat((main_attributes_tensor, self.arc_type)), vehicle_tensors

    def __repr__(self):
        return (f"Arc(id={self.arc_id}, type={self.arc_type.tolist()}, length={self.length} km, "
                f"travel_time={self.travel_time} min, capacity={self.capacity}, traffic_condition={self.traffic_condition}, "
                f"safety={self.safety}, usage_cost={self.usage_cost}, open={self.open}, source={self.source}, "
                f"target={self.target}, vehicles={[v.vehicle_id for v in self.vehicles]})")

# Exemple d'utilisation
if __name__ == "__main__":
    class Vehicle:
        def __init__(self, vehicle_id, in_service, vehicle_type, is_node, location_id, next_departure, capacity, capacity_left, service_hours):
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
            return torch.tensor([
                self.vehicle_id, self.in_service, *self.vehicle_type.tolist(), self.is_node, self.location_id,
                self.next_departure, self.capacity, self.capacity_left, *self.service_hours.tolist()
            ], dtype=torch.float)

    arc = Arc(
        arc_id=1,
        arc_type=torch.tensor([1, 0, 0, 0, 0]),  # One-hot encoded: [road, railway, canal, maritime, air_route]
        length=15.5,
        travel_time=30,
        capacity=100,
        traffic_condition=2,
        safety=8,
        usage_cost=2.5,
        open=1,
        source=1,
        target=2,
        vehicles=[]
    )

    vehicle = Vehicle(
        vehicle_id=2,
        in_service=1,  # 1 for True (in service)
        vehicle_type=torch.tensor([0, 1, 0, 0]),  # One-hot encoded: [Truck, Train, Boat, Plane]
        is_node=0,  # 0 for arc
        location_id=1,
        next_departure=1685241600.0,  # Timestamp
        capacity=100,
        capacity_left=50,
        service_hours=torch.tensor([6.0, 22.0])  # Opening hour: 6, Closing hour: 22
    )

    arc.add_vehicle(vehicle)
    arc_tensor, vehicles_tensor = arc.to_tensor()
    print(arc)
    print(arc_tensor)
    print(vehicles_tensor)
