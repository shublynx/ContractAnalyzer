# Use a slim image for production efficiency
FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Install system-level dependencies for Postgres and C-extensions
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy your project code
COPY . /code/

EXPOSE 8000

# Start the server (Development mode)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]