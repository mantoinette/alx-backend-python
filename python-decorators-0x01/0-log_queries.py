import sqlite3
import functools
import os
from datetime import datetime

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(query, *args, **kwargs):
        print(f"Executing query: {query}")  # Log the SQL query
        return func(query, *args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")

# Define the file path
file_path = '0-log_queries.py'

# Check if the file exists and is not empty
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print(f"{file_path} exists and is not empty.")
    
    # Check if the file contains the specified import statement
    with open(file_path, 'r') as file:
        content = file.read()
        if "from datetime import datetime" in content:
            print(f"{file_path} contains the import statement.")
        else:
            print(f"{file_path} does not contain the import statement.")
else:
    print(f"{file_path} does not exist or is empty.")
