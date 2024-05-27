import pandas as pd

# Process nodes :

df = pd.read_csv('raw_data/nodes.csv')

type_dummies = pd.get_dummies(df['Type']).astype(int)

# Separate 'Coordinates' into two columns
df[['Latitude', 'Longitude']] = df['Coordinates'].str.extract(r'\(([^,]+), ([^)]+)\)').astype(float)

# Split 'Resource_Availability' into 'Vehicle_Availability' and 'Driver_Availability'
df[['Vehicle_Availability', 'Driver_Availability']] = df['Resource_Availability'].str.extract(r'(\d+) \w+, (\d+) \w+')
df['Driver_Availability'] = df['Driver_Availability'].fillna(0).astype(int)
df['Vehicle_Availability'] = df['Vehicle_Availability'].fillna(0).astype(int)

def convert_time_to_decimal(time_str):
    time_str = time_str.replace('"', '').strip()
    if time_str == "24 hours":
        return 24.0, 24.0
    else:
        start, end = time_str.split('-')
        start_hour, start_minute = map(int, start.split(':'))
        end_hour, end_minute = map(int, end.split(':'))
        start_decimal = start_hour + start_minute / 60
        end_decimal = end_hour + end_minute / 60
        return start_decimal, end_decimal

# Convert 'Operating Hours' into 'Opening Hours' and 'Closing Hours'
df['Opening_Hours'], df['Closing_Hours'] = zip(*df['Operating_Hours'].apply(convert_time_to_decimal))


# Drop original columns that were split or encoded
df.drop(['Type', 'Coordinates', 'Resource_Availability', 'Operating_Hours'], axis=1, inplace=True)

# Merge the one-hot encoded 'Type' dataframe
df = pd.concat([df, type_dummies], axis=1)

# Print the processed DataFrame
print(df)

df.to_csv('processed_data/processed_nodes.csv', index=False)

# Process arcs :

#pd.set_option('display.max_columns', None)  # None means unlimited
#pd.set_option('display.width', None)        # Use None to ensure it tries to use maximum space available
#pd.set_option('display.max_colwidth', None)

# Assuming you have already loaded and processed your DataFrame
# Load data from arcs.csv (or use existing df if already loaded and processed)
df = pd.read_csv('structured_data/structured_arcs.csv')

traffic_conditions_map = {'Low': 0, 'Moderate': 1, 'High': 2}
infrastructure_quality_map = {'Poor': 0, 'Average': 1, 'Good': 2}
safety_map = {'Low': 0, 'Medium': 1, 'High': 2}
dynamic_data_map = {'Stable': 0, 'Variable': 1}

df['Traffic_Conditions'] = df['Traffic_Conditions'].replace(traffic_conditions_map)
df['Infrastructure_Quality'] = df['Infrastructure_Quality'].replace(infrastructure_quality_map)
df['Safety'] = df['Safety'].replace(safety_map)
df['Dynamic_Data'] = df['Dynamic_Data'].replace(dynamic_data_map)

df[['Vehicle_Capacity', 'Passenger_Capacity']] = df['Capacity'].str.extract(r'(\d+)\s\w+,\s(\d+)\s\w+')

# Convert the extracted strings to numeric values
df['Vehicle_Capacity'] = pd.to_numeric(df['Vehicle_Capacity'])
df['Passenger_Capacity'] = pd.to_numeric(df['Passenger_Capacity'])

df.drop('Capacity', axis=1, inplace=True)


# Process 'Maintenance' to extract cost and maintenance (continuing from previous data processing)
df['Cost'] = df['Usage_Cost'].str.extract(r'(\$[\d]+)').replace(r'\$', '', regex=True).astype(float)
df['Maintenance'] = df['Usage_Cost'].str.extract(r',\s(.+)')[0]

# Replace 'Low', 'Moderate', and 'High' in 'Maintenance' with 0, 1, and 2
maintenance_map = {'Low maintenance': 0, 'Moderate maintenance': 1, 'High maintenance': 2}
df['Maintenance'] = df['Maintenance'].map(maintenance_map)

# Drop the original 'Usage_Cost' column if no longer needed
df.drop('Usage_Cost', axis=1, inplace=True)

# Example of one-hot encoding for 'Type' and merging back if needed (already done in previous steps)
type_dummies = pd.get_dummies(df['Type']).astype(int)
df = pd.concat([df, type_dummies], axis=1)
df.drop('Type', axis=1, inplace=True)

# Optionally handle NaNs in 'Accessibility' and 'Dynamic_Data' or any other column needing it
df['Accessibility'] = df['Accessibility'].fillna('Not Specified')
df['Dynamic_Data'] = df['Dynamic_Data'].fillna('Unknown')

# Print the processed DataFrame to verify
columns_to_drop = ['ID', 'Source', 'Target', 'Length_km', 'Travel_Time', 
                   'Maintenance', 'Air_Route', 'Maritime_Route', 'Railway', 'Road']

# Drop the specified columns
#df_dropped = df.drop(columns=columns_to_drop)
df = df.drop(columns="Accessibility")
# Print the DataFrame after dropping the columns
#print(df_dropped.head())
#from pprint import pprint
#pprint(df.head())

# Save the processed DataFrame back to CSV if needed
df.to_csv('processed_data/processed_arcs.csv', index=False)

