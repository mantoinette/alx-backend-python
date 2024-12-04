import os

# Define the file path
file_path = 'alx-backend-python/python-generators-0x00/1-batch_processing.py'

# Check if the file exists and is not empty
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print(f"File '{file_path}' exists and is not empty.")
else:
    print(f"File '{file_path}' does not exist or is empty.")

# Check for the presence of the function stream_users_in_batches(batch_size)
def check_function_existence(file_path, function_name):
    with open(file_path, 'r') as file:
        content = file.read()
        return function_name in content

# Check for the required functions
stream_function_exists = check_function_existence(file_path, 'def stream_users_in_batches(batch_size)')
batch_processing_function_exists = check_function_existence(file_path, 'def batch_processing()')

if stream_function_exists:
    print("Function 'stream_users_in_batches(batch_size)' exists.")
else:
    print("Function 'stream_users_in_batches(batch_size)' does not exist.")

if batch_processing_function_exists:
    print("Function 'batch_processing()' exists.")
else:
    print("Function 'batch_processing()' does not exist.")

# Check for the use of the yield generator in the stream_users_in_batches function
def check_yield_usage(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return 'yield' in content

yield_usage_exists = check_yield_usage(file_path)

if yield_usage_exists:
    print("The 'yield' generator is used in the 'stream_users_in_batches' function.")
else:
    print("The 'yield' generator is not used in the 'stream_users_in_batches' function.")