# --------------------------
# Base image
# --------------------------
FROM python:3.11-slim

# --------------------------
# Environment variables
# --------------------------
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# --------------------------
# Set work directory
# --------------------------
WORKDIR /app

# --------------------------
# Install system dependencies
# --------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# --------------------------
# Copy requirements and install Python dependencies
# --------------------------
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# --------------------------
# Copy project files
# --------------------------
COPY . /app/

# --------------------------
# Collect static files
# --------------------------
RUN python manage.py collectstatic --noinput

# --------------------------
# Expose port for Django
# --------------------------
EXPOSE 8000

# --------------------------
# Default command (Django dev server)
# --------------------------
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
