#!/bin/bash




# Database credentials
DB_USER="root"
DB_PASSWORD="Aa123456789!"
DB_HOST="localhost" # Change if you're using a remote database

# Path to your SQL file
SQL_FILE="final_project.sql"

# Check if the SQL file exists
if [ ! -f "$SQL_FILE" ]; then
    echo "SQL file not found!"
    exit 1
fi

# Execute the SQL file
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD  < $SQL_FILE

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Database imported successfully."
else
    echo "Error occurred during the import."
    exit 1
fi
