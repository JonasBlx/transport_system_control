import pandas as pd
import random
import torch

# Génération des données pour les nœuds
def generate_node_data():
    # Définir les intervalles pour les latitudes et longitudes
    latitude_interval = (34.0, 55.0)
    longitude_interval = (-122.0, 139.0)

    # Générer des latitudes et longitudes aléatoires
    random_latitudes = [round(random.uniform(*latitude_interval), 4) for _ in range(18)]
    random_longitudes = [round(random.uniform(*longitude_interval), 4) for _ in range(18)]

    # Générer des demandes aléatoires
    random_demands = [random.randint(50, 150) for _ in range(18)]

    # Générer des types de nœuds (one-hot encoded)
    node_types = []
    for i in range(18):
        node_type = [0, 0, 0, 0, 0]
        if i % 5 == 0:
            node_type[0] = 1  # Bus stop
        elif i % 5 == 1:
            node_type[1] = 1  # Railway station
        elif i % 5 == 2:
            node_type[2] = 1  # Seaport
        elif i % 5 == 3:
            node_type[3] = 1  # Airport
        else:
            node_type[4] = 1  # Hub
        node_types.append(node_type)

    # Créer les autres données
    data = {
        "node_id": list(range(1, 19)),
        "node_type": node_types,
        "coordinates": list(zip(random_latitudes, random_longitudes)),
        "capacity": [100, 200, 300, 400, 500, 150, 250, 350, 450, 550, 120, 220, 320, 420, 520, 170, 270, 370],
        "vehicles": [[] for _ in range(18)],  # Liste vide pour les véhicules
        "staff": [2, 4, 6, 8, 10, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 3, 5, 7],
        "service_hours": [(6, 22) if i % 2 == 0 else (0, 24) for i in range(18)],  # Ouverture et fermeture
        "demand": random_demands
    }

    # Convertir les données en DataFrame
    df = pd.DataFrame(data)

    # Sauvegarder les données dans un fichier CSV
    df.to_csv("nodes_example_1.csv", index=False)

# Génération des données pour les arcs
def generate_arc_data():
    # Liste des nœuds pour les arcs
    nodes = list(range(1, 19))

    # Générer des données d'arcs
    arc_data = {
        "arc_id": list(range(1, 41)),
        "arc_type": [],
        "length": [],
        "travel_time": [],
        "capacity": [],
        "traffic_condition": [],
        "safety": [],
        "usage_cost": [],
        "open": [],
        "source": [],
        "target": [],
        "vehicles": [[] for _ in range(1,41)]
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

        arc_type_one_hot = [0, 0, 0, 0, 0]
        arc_type_one_hot[arc_types.index(arc_type)] = 1

        arc_data["arc_type"].append(arc_type_one_hot)
        arc_data["length"].append(length)
        arc_data["travel_time"].append(travel_time)
        arc_data["capacity"].append(capacity)
        arc_data["traffic_condition"].append(traffic_condition)
        arc_data["safety"].append(safety)
        arc_data["usage_cost"].append(usage_cost)
        arc_data["open"].append(open_status)
        arc_data["source"].append(source)
        arc_data["target"].append(target)

    # Convertir les données en DataFrame
    arc_df = pd.DataFrame(arc_data)

    # Sauvegarder les données dans un fichier CSV
    arc_df.to_csv("arcs_example_1.csv", index=False)

# Exécuter les fonctions pour générer et sauvegarder les données
generate_node_data()
generate_arc_data()
