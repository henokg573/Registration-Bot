# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevent Python from writing .pyc files
ENV PYTHONUNBUFFERED 1        # Ensure output is sent straight to terminal (no buffering)

# Set the working directory
WORKDIR /app

# Copy project files into the container
COPY . /app/

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the app port
EXPOSE 10000

# Run a production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "register:app"]
