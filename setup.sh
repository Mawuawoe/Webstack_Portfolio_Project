#!/bin/bash

# Create a virtual environment if it doesn't already exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Install dependencies
echo "Installing dependencies..."
./venv/bin/pip install -r requirements.txt

# Set up MySQL database and user using the external SQL file
SQL_FILE="./Salinity_web_app/utils/setup_mysql.sql"
if [ -f "$SQL_FILE" ]; then
    echo "Setting up MySQL database and user..."
    mysql -u root -p < "$SQL_FILE"
else
    echo "Error: SQL setup file not found at $SQL_FILE"
    exit 1
fi

# Export environment variables
export MYSQL_USER=salinity
export MYSQL_PWD=admin_pwd
export MYSQL_HOST=localhost
export MYSQL_DB=salinity_db
export TYPE_OF_STORAGE=db

# Navigate to the Flask app directory
cd ./Salinity_web_app || { echo "Directory not found! Exiting."; exit 1; }

# Run the Flask app using the virtual environment
echo "Starting the Flask app..."
../venv/bin/python app.py
