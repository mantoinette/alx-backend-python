def stream_user_ages():
    """Generator function to yield user ages one by one."""
    ages = [22, 25, 30, 28, 35, 40, 18, 50]  # Example user ages
    for age in ages:
        yield age

def calculate_average_age():
    """Calculate the average age of users using the stream_user_ages generator."""
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    return total_age / count if count > 0 else 0

# Example usage
if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")
