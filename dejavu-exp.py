import psycopg2
from dejavu import Dejavu
from dejavu.logic.recognizer.file_recognizer import FileRecognizer
import os
from dotenv import load_dotenv
load_dotenv()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname = os.getenv('dbname'),
    user = os.getenv('user'),
    password = os.getenv('password'),
    host = os.getenv('host'),
    port = os.getenv('port')
)

# Initialize Dejavu with the appropriate configuration
config = {
    "database": {
        "host": os.getenv('host'),
        "user": os.getenv('user'),
        "password": os.getenv('password'),
        "database": os.getenv('dbname'),
    }
}
djv = Dejavu(config)

# Create a cursor object
cursor = conn.cursor()

# Query to retrieve fingerprints from the fingerprints table
fingerprint_query = """
    SELECT hash
    FROM fingerprints;
"""

# Execute the query to retrieve the fingerprints
cursor.execute(fingerprint_query)
fingerprints = cursor.fetchall()

# Iterate over each fingerprint and recognize it against the songs table
for fingerprint_data in fingerprints:
    fingerprint_data = fingerprint_data[0]
    song = djv.recognize(FileRecognizer, fp=fingerprint_data)
    if song is not None:
        print("Match found for fingerprint:", fingerprint_data)
        print("Matched song:", song)
        # Handle the match as needed
    else:
        print("No match found for fingerprint:", fingerprint_data)
        # Handle the non-match as needed

# Close the cursor and the database connection
cursor.close()
conn.close()
