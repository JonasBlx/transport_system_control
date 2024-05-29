import pandas as pd
import ast

def check_unique_node_types(df):
    for index, row in df.iterrows():
        node_type = ast.literal_eval(row['node_type'])
        if sum(node_type) != 1:
            print(f"Error: Node ID {row['node_id']} has {sum(node_type)} types set to 1. Each node must have exactly one type.")
            return False
    return True

def check_latitude_longitude(df):
    for index, row in df.iterrows():
        coordinates = ast.literal_eval(row['coordinates'])
        latitude, longitude = coordinates
        if not (-90 <= latitude <= 90):
            print(f"Error: Node ID {row['node_id']} has invalid latitude {latitude}. Latitude must be between -90 and 90.")
            return False
        if not (-180 <= longitude <= 180):
            print(f"Error: Node ID {row['node_id']} has invalid longitude {longitude}. Longitude must be between -180 and 180.")
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
        if row['staff'] < 0:
            print(f"Error: Node ID {row['node_id']} has negative number of staff {row['staff']}.")
            return False
    return True

def check_operating_hours(df):
    for index, row in df.iterrows():
        service_hours = ast.literal_eval(row['service_hours'])
        opening_hours, closing_hours = service_hours
        if not (0 <= opening_hours <= 24):
            print(f"Error: Node ID {row['node_id']} has invalid opening hours {opening_hours}. Opening hours must be between 0 and 24.")
            return False
        if not (0 <= closing_hours <= 24):
            print(f"Error: Node ID {row['node_id']} has invalid closing hours {closing_hours}. Closing hours must be between 0 and 24.")
            return False
        if opening_hours == closing_hours and opening_hours != 24:
            print(f"Error: Node ID {row['node_id']} has same opening and closing hours {opening_hours}, which is not allowed unless it's 24/24 (24, 24).")
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
