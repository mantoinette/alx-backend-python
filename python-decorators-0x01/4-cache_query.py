import time
import sqlite3 
import functools

query_cache = {}

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

def cache_query(func):
    """Decorator that caches query results based on the SQL query string."""
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]  # Return cached result if available
        else:
            print("Executing query and caching result:", query)
            result = func(conn, query)  # Execute the query
            query_cache[query] = result  # Cache the result
            return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
