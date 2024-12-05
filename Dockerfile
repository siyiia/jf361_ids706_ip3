# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application's dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the required model to avoid runtime delays
RUN python -c "from transformers import pipeline; pipeline('text-generation', model='gpt2')"

# Copy the application code
COPY . .

# Expose the application port
EXPOSE 8501

# Command to run the application
CMD ["python", "app.py"]
