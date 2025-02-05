# Use a base Python image (python 3.10)
FROM python:3.10
# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app code into the container
COPY . .

# Expose port 8000 (default port for Django)
EXPOSE 8000

# Command to run your Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
