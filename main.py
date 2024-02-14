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

# Retrieve Songs from the database
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM songs")
    songs_in_db = cursor.fetchall()
    print("Songs retrieved from the database:", songs_in_db)
except Exception as e:
    print("Error retrieving fingerprints from the database:", e)

# Retrieve Fingerprints from the database
try:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fingerprints")
    fingerprints_in_db = cursor.fetchall()
    print("Fingerprints retrieved from the database:", fingerprints_in_db)
except Exception as e:
    print("Error retrieving fingerprints from the database:", e)

# Compare fingerprints
for fingerprint in fingerprints_in_db:
    if fingerprint in songs_in_db:
        print("Fingerprint", fingerprint, "exists in the songs table.")
    else:
        print("Fingerprint", fingerprint, "does not exist in the songs table.")

# Close the cursor and the connection
cursor.close()
conn.close()
