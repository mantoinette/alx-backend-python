class ExecuteQuery:
    def __init__(self, query, param):
        self.query = query
        self.param = param
        self.connection = None  # Placeholder for database connection

    def __enter__(self):
        # Establish the database connection here
        self.connection = self.create_connection()  # Implement this method
        return self.execute_query()  # Execute the query and return the result

    def __exit__(self, exc_type, exc_value, traceback):
        # Close the database connection here
        if self.connection:
            self.connection.close()  # Ensure the connection is closed

    def create_connection(self):
        # Logic to create and return a database connection
        pass  # Replace with actual implementation

    def execute_query(self):
        # Logic to execute the query and return results
        pass  # Replace with actual implementation

# Usage example
with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as result:
    print(result)  # Process the result as needed
