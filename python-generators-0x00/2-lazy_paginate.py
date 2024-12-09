def paginate_users(page_size, offset):
    """Simulate fetching users from a data source."""
    # Simulating SQL-like pagination
    users = range(1, 101)  # Example user IDs from 1 to 100
    return users[offset:offset + page_size]  # This simulates "SELECT * FROM user_data LIMIT page_size OFFSET offset"

def lazy_paginate(page_size):
    """Generator function to yield users in pages."""
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # If no more users are returned, stop the generator
            break
        yield page
        offset += page_size  # Move to the next offset

# Example usage of the lazy_paginate generator
if __name__ == "__main__":
    page_size = 10  # Define the size of each page
    paginator = lazy_paginate(page_size)

    for page in paginator:
        print(list(page))  # Print each page of users
