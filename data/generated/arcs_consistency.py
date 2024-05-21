import pandas as pd

def check_unique_arc_types(df):
    arc_types = ['road', 'railway', 'canal', 'maritime', 'air_route']
    for index, row in df.iterrows():
        type_count = sum([row[arc_type] for arc_type in arc_types])
        if type_count != 1:
            print(f"Error: Arc ID {row['arc_id']} has {type_count} types set to 1. Each arc must have exactly one type.")
            return False
    return True

def check_positive_length_travel_time(df):
    for index, row in df.iterrows():
        if row['length'] <= 0:
            print(f"Error: Arc ID {row['arc_id']} has non-positive length {row['length']}. Length must be greater than 0.")
            return False
        if row['travel_time'] <= 0:
            print(f"Error: Arc ID {row['arc_id']} has non-positive travel time {row['travel_time']}. Travel time must be greater than 0.")
            return False
    return True

def check_positive_capacity(df):
    for index, row in df.iterrows():
        if row['capacity'] <= 0:
            print(f"Error: Arc ID {row['arc_id']} has non-positive capacity {row['capacity']}. Capacity must be greater than 0.")
            return False
    return True

def check_traffic_condition(df):
    for index, row in df.iterrows():
        if row['traffic_condition'] not in [0, 1, 2]:
            print(f"Error: Arc ID {row['arc_id']} has invalid traffic condition {row['traffic_condition']}. Must be 0 (poor), 1 (average), or 2 (good).")
            return False
    return True

def check_safety(df):
    for index, row in df.iterrows():
        if not (0 <= row['safety'] <= 10):
            print(f"Error: Arc ID {row['arc_id']} has invalid safety {row['safety']}. Safety must be between 0 and 10.")
            return False
    return True

def check_usage_cost(df):
    for index, row in df.iterrows():
        if row['usage_cost'] < 0:
            print(f"Error: Arc ID {row['arc_id']} has negative usage cost {row['usage_cost']}. Usage cost must be non-negative.")
            return False
    return True

def check_open(df):
    for index, row in df.iterrows():
        if row['open'] not in [0, 1]:
            print(f"Error: Arc ID {row['arc_id']} has invalid open value {row['open']}. Must be 0 (closed) or 1 (open).")
            return False
    return True

def check_csv_file(file_path):
    df = pd.read_csv(file_path)
    
    checks = [
        ("Unique Arc Types", check_unique_arc_types),
        ("Positive Length and Travel Time", check_positive_length_travel_time),
        ("Positive Capacity", check_positive_capacity),
        ("Traffic Condition", check_traffic_condition),
        ("Safety", check_safety),
        ("Usage Cost", check_usage_cost),
        ("Open", check_open)
    ]
    
    all_checks_passed = True
    for check_name, check_function in checks:
        print(f"Performing check: {check_name}")
        if not check_function(df):
            all_checks_passed = False
            print(f"Check failed: {check_name}")
        else:
            print(f"Check passed: {check_name}")
        print()
    
    if all_checks_passed:
        print("All checks passed. The CSV file is consistent.")
    else:
        print("Some checks failed. Please review the errors.")

if __name__ == "__main__":
    file_path = "arcs_example_1.csv"
    check_csv_file(file_path)
