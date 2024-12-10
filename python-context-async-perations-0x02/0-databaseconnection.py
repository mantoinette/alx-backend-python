class DatabaseConnection:
    """Context manager for database connection."""
    
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
    page_size = 10  # Define the size of each page
    paginator = lazy_paginate(page_size)

    for page in paginator:
        print(list(page))  # Print each page of users

    # Using the DatabaseConnection context manager
    with DatabaseConnection() as db:
        results = db.query("SELECT * FROM users")
        print(results)  # Print the results from the query
