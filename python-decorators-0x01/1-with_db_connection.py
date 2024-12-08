import os
import sqlite3 
import functools

# Check if the file exists and is not empty
file_path = 'alx-backend-python/python-decorators-0x01/1-with_db_connection.py'

if os.path.isfile(file_path) and os.path.getsize(file_path) > 0:
    print("The file exists and is not empty.")
else:
    print("The file either does not exist or is empty.")

def with_db_connection(func):
    """Decorator that opens a database connection and closes it after the function call."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('your_database.db')  # Specify your database file
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()  # Ensure the connection is closed after the function call
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

# Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=1)
print(user)
