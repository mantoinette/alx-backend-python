import os

# Check if the file exists and is not empty
file_path = 'alx-backend-python/python-context-async-perations-0x02/0-databaseconnection.py'

if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print(f"{file_path} exists and is not empty.")
else:
    print(f"{file_path} does not exist or is empty.")

class DatabaseConnection:
    """Context manager for database connection."""
    
    def __init__(self):
        # Initialize any necessary attributes
        self.connection = None

    def __enter__(self):
        # Simulate opening a database connection
        self.connection = "Database connection established"
        return self  # Return the connection object

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Simulate closing the database connection
        self.connection = None
        print("Database connection closed")

    def query(self, sql):
        # Simulate executing a query and returning results
        if sql == "SELECT * FROM users":
            return ["User1", "User2", "User3"]  # Example user data
        return []

# Example usage of the DatabaseConnection context manager
if __name__ == "__main__":
    # Using the DatabaseConnection context manager
    with DatabaseConnection() as db:
        results = db.query("SELECT * FROM users")
        print(results)  # Print the results from the query
