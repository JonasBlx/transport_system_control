import pandas as pd

# Exemple de données de nœuds avec 18 nœuds
data = {
    "node_id": list(range(1, 19)),
    "bus_stop": [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    "railway_station": [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    "seaport": [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    "airport": [0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    "hub": [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    "latitude": [48.8566, 51.5074, 40.7128, 35.6895, 34.0522, 37.7749, 55.7558, 39.9042, 52.5200, 45.4642, 19.0760, 13.7563, -33.8688, 41.9028, 35.6762, 34.6937, 31.2304, -23.5505],
    "longitude": [2.3522, -0.1278, -74.0060, 139.6917, -118.2437, -122.4194, 37.6173, 116.4074, 13.4050, 9.1900, 72.8777, 100.5018, 151.2093, 12.4964, 139.6503, 135.5023, 121.4737, -46.6333],
    "capacity": [100, 200, 300, 400, 500, 150, 250, 350, 450, 550, 120, 220, 320, 420, 520, 170, 270, 370],
    "vehicles": [5, 10, 15, 20, 25, 6, 11, 16, 21, 26, 7, 12, 17, 22, 27, 8, 13, 18],
    "staff": [2, 4, 6, 8, 10, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 3, 5, 7],
    "opening_hours": [6, 5, 24, 7, 24, 6, 5, 24, 7, 24, 6, 5, 24, 7, 24, 6, 5, 24],
    "closing_hours": [22, 23, 24, 21, 24, 22, 23, 24, 21, 24, 22, 23, 24, 21, 24, 22, 23, 24]
}

# Créer un DataFrame
df = pd.DataFrame(data)

# Sauvegarder les données dans un fichier CSV
df.to_csv("nodes_example_1.csv", index=False)

import pandas as pd
import random

# Liste des nœuds pour les arcs
nodes = list(range(1, 19))

# Générer des données d'arcs
arc_data = {
    "arc_id": list(range(1, 41)),
    "road": [],
    "railway": [],
    "canal": [],
    "maritime": [],
    "air_route": [],
    "length": [],
    "travel_time": [],
    "capacity": [],
    "traffic_condition": [],
    "safety": [],
    "usage_cost": [],
    "open": [],
    "source": [],
    "target": []
}

# Définir les types d'arc disponibles
arc_types = ['road', 'railway', 'canal', 'maritime', 'air_route']

for arc_id in arc_data["arc_id"]:
    arc_type = random.choice(arc_types)
    length = round(random.uniform(1.0, 50.0), 2)
    travel_time = round(random.uniform(10.0, 60.0), 2)
    capacity = random.randint(100, 500)
    traffic_condition = random.randint(0, 2)
    safety = random.randint(0, 10)
    usage_cost = round(random.uniform(1.0, 5.0), 2)
    open_status = random.randint(0, 1)
    source = random.choice(nodes)
    target = random.choice([n for n in nodes if n != source])  # Ensure source and target are different

    arc_data["road"].append(1 if arc_type == 'road' else 0)
    arc_data["railway"].append(1 if arc_type == 'railway' else 0)
    arc_data["canal"].append(1 if arc_type == 'canal' else 0)
    arc_data["maritime"].append(1 if arc_type == 'maritime' else 0)
    arc_data["air_route"].append(1 if arc_type == 'air_route' else 0)
    arc_data["length"].append(length)
    arc_data["travel_time"].append(travel_time)
    arc_data["capacity"].append(capacity)
    arc_data["traffic_condition"].append(traffic_condition)
    arc_data["safety"].append(safety)
    arc_data["usage_cost"].append(usage_cost)
    arc_data["open"].append(open_status)
    arc_data["source"].append(source)
    arc_data["target"].append(target)

# Créer un DataFrame
arc_df = pd.DataFrame(arc_data)

# Sauvegarder les données dans un fichier CSV
arc_df.to_csv("arcs_example_1.csv", index=False)

