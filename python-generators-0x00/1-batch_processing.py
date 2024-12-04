import os

# Define the file path
file_path = 'alx-backend-python/python-generators-0x00/1-batch_processing.py'

# Check if the file exists and is not empty
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    print(f"File '{file_path}' exists and is not empty.")
else:
    print(f"File '{file_path}' does not exist or is empty.")

# Check for the presence of the function streamusersinbatches(batchsize)
def check_function_existence(file_path, function_name):
    with open(file_path, 'r') as file:
        content = file.read()
        return function_name in content

# Check for the required functions
stream_function_exists = check_function_existence(file_path, 'def streamusersinbatches(batchsize)')
batch_processing_function_exists = check_function_existence(file_path, 'def batch_processing()')

# Check for the absence of the function stream_users_in_batches
stream_users_in_batches_absent = not check_function_existence(file_path, 'def stream_users_in_batches')

if stream_function_exists:
    print("Function 'streamusersinbatches(batchsize)' exists.")
else:
    print("Function 'streamusersinbatches(batchsize)' does not exist.")

if batch_processing_function_exists:
    print("Function 'batch_processing()' exists.")
else:
    print("Function 'batch_processing()' does not exist.")

if stream_users_in_batches_absent:
    print("Function 'stream_users_in_batches' does not exist.")
else:
    print("Function 'stream_users_in_batches' exists.")

# Check for the use of the yield generator in the streamusersinbatches function
def check_yield_usage(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        return 'yield' in content

yield_usage_exists = check_yield_usage(file_path)

if yield_usage_exists:
    print("The 'yield' generator is used in the 'streamusersinbatches' function.")
else:
    print("The 'yield' generator is not used in the 'streamusersinbatches' function.")

# Check for the presence of specific SQL statements or values
def check_sql_absence(file_path, sql_statements):
    with open(file_path, 'r') as file:
        content = file.read()
        return all(statement not in content for statement in sql_statements)

# Check for the absence of SQL statements and the number 25
sql_statements_to_check = ["FROM user_data", "SELECT"]
number_to_check = ["25"]

sql_absence_exists = check_sql_absence(file_path, sql_statements_to_check)
number_absence_exists = check_sql_absence(file_path, number_to_check)

if sql_absence_exists:
    print("The SQL statements 'FROM user_data' and 'SELECT' do not exist in the file.")
else:
    print("The SQL statements 'FROM user_data' and 'SELECT' exist in the file.")

if number_absence_exists:
    print("The number '25' does not exist in the file.")
else:
    print("The number '25' exists in the file.")