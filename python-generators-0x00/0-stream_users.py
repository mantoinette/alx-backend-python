#!/usr/bin/python3
from itertools import islice
import sqlite3  # Import the sqlite3 module to interact with SQLite databases

def stream_users():
    """Generator function to fetch rows from the user_data table one by one."""
    connection = sqlite3.connect('alx.db')  # Connect to the SQLite database (replace with your database)
    cursor = connection.cursor()  # Create a cursor object to execute SQL commands
    
    cursor.execute("SELECT * FROM user_data")  # Execute a SQL query to select all rows from the user_data table
    for row in cursor.fetchall():  # Fetch all rows returned by the query
        yield row  # Yield each row one by one, making this a generator function

    cursor.close()  # Close the cursor to free up resources
    connection.close()  # Close the database connection

# Example usage
if __name__ == "__main__":
    # Iterate over the generator function and print only the first 6 rows
    for user in islice(stream_users(), 6):  # Use islice to limit the output to the first 6 users
        print(user)  # Print each user row
