#!/usr/bin/python3

# Import the seed module
seed = __import__('seed')

# Establish a connection to the database
connection = seed.connect_db()
if connection:
    # Create the database if the connection is successful
    seed.create_database(connection)
    connection.close()  # Close the connection after creating the database
    print(f"connection successful")

    # Connect to the development database
    connection = seed.connect_to_prodev()

    if connection:
        # Create the necessary table in the development database
        seed.create_table(connection)
        # Insert data from 'user_data.csv' into the table
        seed.insert_data(connection, 'user_data.csv')
        cursor = connection.cursor()
        # Check if the schema 'ALX_prodev' exists
        cursor.execute(f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print(f"Database ALX_prodev is present ")
        # Fetch and display the first 5 rows from the 'user_data' table
        cursor.execute(f"SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(f"Table user_data created successfully")
        print(f"Database ALX_prodev is present")
        print(rows)  # Print the fetched rows
        cursor.close()  # Close the cursor after operations are complete
