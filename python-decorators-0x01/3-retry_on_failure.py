import sqlite3 
import functools

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

def transactional(func):
    """Decorator that wraps a function in a database transaction."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit the transaction if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback the transaction if an error occurs
            print(f"Transaction failed: {e}")
            raise  # Re-raise the exception for further handling
    return wrapper

@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 

# Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
