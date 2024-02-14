import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


# PostgreSQL connection parameters
dbname = os.getenv('dbname')
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')

# Connect to the PostgreSQL database
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    print("Connected to the PostgreSQL database.")
except Exception as e:
    print("Unable to connect to the database:", e)

# Execute SQL queries
try:
    # Create a cursor object
    cursor = conn.cursor()

    # Execute a simple SQL query
    cursor.execute("SELECT * FROM fingerprints")

    # Fetch the results
    rows = cursor.fetchall()

    # Process the results
    for row in rows:
        print(row)

    # Close the cursor
    cursor.close()
except Exception as e:
    print("Error executing SQL query:", e)

# Close the database connection
conn.close()
