class Node:
    def __init__(self, node_id, bus_stop, railway_station, seaport, airport, hub, latitude, longitude, capacity, vehicles, staff, opening_hours, closing_hours):
        """
        Initialize a node in the transportation network.
        
        Args:
            node_id (int): Unique identifier for the node.
            bus_stop (int): 1 if the node is a bus stop, else 0.
            railway_station (int): 1 if the node is a railway station, else 0.
            seaport (int): 1 if the node is a seaport, else 0.
            airport (int): 1 if the node is an airport, else 0.
            hub (int): 1 if the node is a hub, else 0.
            latitude (float): Latitude of the node.
            longitude (float): Longitude of the node.
            capacity (int): Capacity for handling passengers simultaneously.
            vehicles (int): Number of vehicles available at the node.
            staff (int): Number of staff available at the node.
            opening_hours (int): Opening hour of the node.
            closing_hours (int): Closing hour of the node.
        """
        self.node_id = node_id
        self.bus_stop = bus_stop
        self.railway_station = railway_station
        self.seaport = seaport
        self.airport = airport
        self.hub = hub
        self.latitude = latitude
        self.longitude = longitude
        self.capacity = capacity
        self.vehicles = vehicles
        self.staff = staff
        self.opening_hours, self.closing_hours = self._process_operating_hours(opening_hours, closing_hours)

    def _process_operating_hours(self, opening_hours, closing_hours):
        if opening_hours == 0 and closing_hours == 24:
            return 0, 0
        return opening_hours, closing_hours

    def get_id(self):
        return self.node_id

    def get_coordinates(self):
        return self.latitude, self.longitude

    def get_capacity(self):
        return self.capacity

    def get_vehicles(self):
        return self.vehicles

    def get_staff(self):
        return self.staff

    def get_operating_hours(self):
        return self.opening_hours, self.closing_hours

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
        if self.opening_hours == 0 and self.closing_hours == 0:
            return True
        return self.opening_hours <= current_hour < self.closing_hours

    def __repr__(self):
        return (f"Node(id={self.node_id}, bus_stop={self.bus_stop}, railway_station={self.railway_station}, "
                f"seaport={self.seaport}, airport={self.airport}, hub={self.hub}, latitude={self.latitude}, "
                f"longitude={self.longitude}, capacity={self.capacity}, vehicles={self.vehicles}, staff={self.staff}, "
                f"operating_hours=({self.opening_hours}, {self.closing_hours}))")

# Example usage
if __name__ == "__main__":
    node = Node(
        node_id=1,
        bus_stop=1,
        railway_station=0,
        seaport=0,
        airport=0,
        hub=0,
        latitude=48.8566,
        longitude=2.3522,
        capacity=100,
        vehicles=5,
        staff=2,
        opening_hours=6,
        closing_hours=22
    )
    print(node)
