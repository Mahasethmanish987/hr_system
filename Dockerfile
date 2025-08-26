# Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Use the entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
