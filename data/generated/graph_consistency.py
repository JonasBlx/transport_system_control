import pandas as pd

def load_nodes(file_path):
    return pd.read_csv(file_path)

def load_arcs(file_path):
    return pd.read_csv(file_path)

def check_node_existence(df_nodes, df_arcs):
    node_ids = set(df_nodes["node_id"])
    for index, row in df_arcs.iterrows():
        if row["source"] not in node_ids:
            print(f"Error: Arc ID {row['arc_id']} has a source node {row['source']} that does not exist.")
            return False
        if row["target"] not in node_ids:
            print(f"Error: Arc ID {row['arc_id']} has a target node {row['target']} that does not exist.")
            return False
    return True

def check_unique_arc_types(df_arcs):
    arc_types = ['road', 'railway', 'canal', 'maritime', 'air_route']
    for index, row in df_arcs.iterrows():
        type_count = sum([row[arc_type] for arc_type in arc_types])
        if type_count != 1:
            print(f"Error: Arc ID {row['arc_id']} has {type_count} types set to 1. Each arc must have exactly one type.")
            return False
    return True

def check_positive_length_travel_time(df_arcs):
    for index, row in df_arcs.iterrows():
        if row['length'] <= 0:
            print(f"Error: Arc ID {row['arc_id']} has non-positive length {row['length']}. Length must be greater than 0.")
            return False
        if row['travel_time'] <= 0:
            print(f"Error: Arc ID {row['arc_id']} has non-positive travel time {row['travel_time']}. Travel time must be greater than 0.")
            return False
    return True

def check_positive_capacity(df_arcs):
    for index, row in df_arcs.iterrows():
        if row['capacity'] <= 0:
            print(f"Error: Arc ID {row['arc_id']} has non-positive capacity {row['capacity']}. Capacity must be greater than 0.")
            return False
    return True

def check_traffic_condition(df_arcs):
    for index, row in df_arcs.iterrows():
        if row['traffic_condition'] not in [0, 1, 2]:
            print(f"Error: Arc ID {row['arc_id']} has invalid traffic condition {row['traffic_condition']}. Must be 0 (poor), 1 (average), or 2 (good).")
            return False
    return True

def check_safety(df_arcs):
    for index, row in df_arcs.iterrows():
        if not (0 <= row['safety'] <= 10):
            print(f"Error: Arc ID {row['arc_id']} has invalid safety {row['safety']}. Safety must be between 0 and 10.")
            return False
    return True

def check_usage_cost(df_arcs):
    for index, row in df_arcs.iterrows():
        if row['usage_cost'] < 0:
            print(f"Error: Arc ID {row['arc_id']} has negative usage cost {row['usage_cost']}. Usage cost must be non-negative.")
            return False
    return True

def check_open(df_arcs):
    for index, row in df_arcs.iterrows():
        if row['open'] not in [0, 1]:
            print(f"Error: Arc ID {row['arc_id']} has invalid open value {row['open']}. Must be 0 (closed) or 1 (open).")
            return False
    return True

def check_csv_files(node_file_path, arc_file_path):
    df_nodes = load_nodes(node_file_path)
    df_arcs = load_arcs(arc_file_path)
    
    checks = [
        ("Node Existence", lambda: check_node_existence(df_nodes, df_arcs)),
        ("Unique Arc Types", lambda: check_unique_arc_types(df_arcs)),
        ("Positive Length and Travel Time", lambda: check_positive_length_travel_time(df_arcs)),
        ("Positive Capacity", lambda: check_positive_capacity(df_arcs)),
        ("Traffic Condition", lambda: check_traffic_condition(df_arcs)),
        ("Safety", lambda: check_safety(df_arcs)),
        ("Usage Cost", lambda: check_usage_cost(df_arcs)),
        ("Open", lambda: check_open(df_arcs))
    ]
    
    all_checks_passed = True
    for check_name, check_function in checks:
        print(f"Performing check: {check_name}")
        if not check_function():
            all_checks_passed = False
            print(f"Check failed: {check_name}")
        else:
            print(f"Check passed: {check_name}")
        print()
    
    if all_checks_passed:
        print("All checks passed. The CSV files are consistent.")
    else:
        print("Some checks failed. Please review the errors.")

if __name__ == "__main__":
    node_file_path = "nodes_example_1.csv"
    arc_file_path = "arcs_example_1.csv"
    check_csv_files(node_file_path, arc_file_path)
