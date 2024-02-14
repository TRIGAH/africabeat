import psycopg2
import os
import hashlib
import json
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
    cursor.execute("SELECT file_sha1 FROM songs")
    songs_in_db = cursor.fetchall()
    # print("Songs retrieved from the database:", songs_in_db)
except Exception as e:
    print("Error retrieving fingerprints from the database:", e)

# Retrieve Fingerprints from the database
try:
    cursor = conn.cursor()
    cursor.execute("SELECT hash FROM fingerprints")
    fingerprints_in_db = cursor.fetchall()
    # print("Fingerprints retrieved from the database:", fingerprints_in_db)
except Exception as e:
    print("Error retrieving fingerprints from the database:", e)


# Compare fingerprints
for fingerprint in fingerprints_in_db[1:5]:
    fingerprint_hash_object = hashlib.sha256(b''.join(fingerprint))
    fingerprint_hash_string = fingerprint_hash_object.hexdigest()
    print(fingerprint_hash_string)

    if fingerprint_hash_string in [hashlib.sha256(b''.join(song)).hexdigest() for song in songs_in_db[1:10] ]:
        print("Fingerprint", fingerprint_hash_string, "exists in the songs table.")
    else:
        print("Fingerprint", fingerprint_hash_string, "does not exist in the songs table.")


    # print([hashlib.sha256(b''.join(song)).hexdigest() for song in songs_in_db[1:10] ])

# Close the cursor and the connection
cursor.close()
conn.close()


# figerprints - hash
# songs - file-sha1