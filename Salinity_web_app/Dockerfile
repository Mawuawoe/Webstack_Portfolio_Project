# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Install necessary system dependencies for MySQL client and build tools
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (e.g., mysqlclient)
RUN pip install --upgrade pip && \
    pip install mysqlclient

# Set the working directory in the container to the salinity_web_app directory
WORKDIR /app

# Copy the contents of the local salinity_web_app directory to the /app directory in the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (make sure the database host is correct)
ENV MYSQL_USER=salinity
ENV MYSQL_PWD=admin_pwd
# Update this if MySQL is in another container (e.g., 'db' for Docker Compose)
ENV MYSQL_HOST=db
ENV MYSQL_DB=salinity_db
ENV TYPE_OF_STORAGE=db

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
