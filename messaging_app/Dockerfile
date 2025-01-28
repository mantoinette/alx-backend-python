# Use Python 3.9 as the base image
FROM python:3.10

# Update package lists and install dependencies
RUN apt-get update && apt-get install -y libdbus-1-dev build-essential python3-dev

# Set the working directory inside the container
WORKDIR /app

# Copy your project files to the container
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the app will run on (optional)
EXPOSE 8000

# Command to run the application (adjust it as per your app's entry point)
CMD ["python", "app.py"]
