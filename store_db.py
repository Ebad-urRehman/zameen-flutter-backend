import pandas as pd
import sqlite3
from icecream import ic
import csv

def create_table_from_csv(db_name, csv_file):
    connection = sqlite3.Connection(db_name)
    cursor = connection.cursor()

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  

        table_name = csv_file.split('.')[0]  # Use the CSV filename as table name
        columns = ', '.join([f'{header} TEXT' for header in headers])  # Assuming all columns are text
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

        for row in reader:
            placeholders = ', '.join(['?'] * len(row))  # Create placeholders for values
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)

    connection.commit()
    connection.close()



def fetch_first(records_no):
    connection = sqlite3.Connection('zameen_data.db')
    cursor = connection.cursor()

    query = f"SELECT * FROM zameen_property_data LIMIT {records_no}"
    cursor.execute(query)

    records = cursor.fetchall()

    list_of_records = [list(record) for  record in records]
    print(list_of_records)
    connection.close()

    return records



def query_specific_values(cols, data, limit, offset):
    connection = sqlite3.Connection('zameen_data.db')
    cursor = connection.cursor()
    query_conditions = []

    params = []

    for col in cols:
        if col == 'bedrooms' or col == 'baths':
            num_value = int(data[col])
            query_conditions.append(f"{col} < ?")
            params.extend([num_value])
        elif col == 'area':
            if('area_type' in data):
                area_type = data['area_type']
                area = int(data[col])
                area_value = f'{area} {area_type}'
                query_conditions.append(f"{col} < ?")
                print(area_value)
                params.extend([area_value])
        elif col == 'area_type':
            pass
        else:
            placeholders = ', '.join(['?'] * len(data[col]))
            query_conditions.append(f"{col} IN ({placeholders})")
            params.extend(data[col])


    where_clause = " AND ".join(query_conditions)


    # count query
    count_query = f"SELECT COUNT(*) FROM zameen_property_data WHERE {where_clause}"
    cursor.execute(count_query, params)
    total_records = cursor.fetchone()[0]

    # data query
    query = f"SELECT * FROM zameen_property_data WHERE {where_clause} LIMIT ? OFFSET ?"
    print(query)
    # query = f"SELECT * FROM zameen_property_data WHERE {col} IN ({placeholders}) AND property_type = 'Flat' AND location = 'G-10'"
    params.extend([limit, offset])
    print(query, params)
    cursor.execute(query, params)


    records = cursor.fetchall()
    connection.close()

    list_of_records = [list(record) for  record in records]
    return list_of_records, total_records



def count_records(col, values):
    connection = sqlite3.connect('zameen_data.db')
    cursor = connection.cursor()

    placeholders = ', '.join(['?'] * len(values))
    
    total_records_query = f"SELECT COUNT(*) FROM zameen_property_data WHERE {col} IN ({placeholders})"
    cursor.execute(total_records_query, values)
    
    total_records = cursor.fetchone()[0]
    connection.close()

    return total_records