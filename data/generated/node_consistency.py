import pandas as pd

def check_unique_node_types(df):
    node_types = ['bus_stop', 'railway_station', 'seaport', 'airport', 'hub']
    for index, row in df.iterrows():
        type_count = sum([row[node_type] for node_type in node_types])
        if type_count != 1:
            print(f"Error: Node ID {row['node_id']} has {type_count} types set to 1. Each node must have exactly one type.")
            return False
    return True

def check_latitude_longitude(df):
    for index, row in df.iterrows():
        if not (-90 <= row['latitude'] <= 90):
            print(f"Error: Node ID {row['node_id']} has invalid latitude {row['latitude']}. Latitude must be between -90 and 90.")
            return False
        if not (-180 <= row['longitude'] <= 180):
            print(f"Error: Node ID {row['node_id']} has invalid longitude {row['longitude']}. Longitude must be between -180 and 180.")
            return False
    return True

def check_capacity(df):
    for index, row in df.iterrows():
        if row['capacity'] <= 0:
            print(f"Error: Node ID {row['node_id']} has non-positive capacity {row['capacity']}. Capacity must be greater than 0.")
            return False
    return True

def check_resources(df):
    for index, row in df.iterrows():
        if row['vehicles'] < 0:
            print(f"Error: Node ID {row['node_id']} has negative number of vehicles {row['vehicles']}.")
            return False
        if row['staff'] < 0:
            print(f"Error: Node ID {row['node_id']} has negative number of staff {row['staff']}.")
            return False
    return True

def check_operating_hours(df):
    for index, row in df.iterrows():
        if not (0 <= row['opening_hours'] <= 24):
            print(f"Error: Node ID {row['node_id']} has invalid opening hours {row['opening_hours']}. Opening hours must be between 0 and 24.")
            return False
        if not (0 <= row['closing_hours'] <= 24):
            print(f"Error: Node ID {row['node_id']} has invalid closing hours {row['closing_hours']}. Closing hours must be between 0 and 24.")
            return False
        if row['opening_hours'] == row['closing_hours'] and row['opening_hours'] != 24:
            print(f"Error: Node ID {row['node_id']} has same opening and closing hours {row['opening_hours']}, which is not allowed unless it's 24/24 (24, 24).")
            return False
    return True

def check_csv_file(file_path):
    df = pd.read_csv(file_path)
    
    checks = [
        ("Unique Node Types", check_unique_node_types),
        ("Latitude and Longitude", check_latitude_longitude),
        ("Capacity", check_capacity),
        ("Resources", check_resources),
        ("Operating Hours", check_operating_hours)
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
    file_path = "nodes_example_1.csv"
    check_csv_file(file_path)
