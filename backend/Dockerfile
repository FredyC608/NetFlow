# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies (needed for Postgres & compilation)
RUN apt-get update && apt-get install -y \
    build-essential \   
    cmake \             
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your backend code
COPY . .

RUN pip install .

# (Optional) Default command, though docker-compose usually overrides this
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]