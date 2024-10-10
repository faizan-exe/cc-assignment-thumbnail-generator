# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set environment variables to avoid interactive prompts
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Define the command to run the application
CMD ["python", "main.py"]
