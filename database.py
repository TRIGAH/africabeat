import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_database(dbname, user, password, host, port):
    try:
        connection = psycopg2.connect(
            dbname='postgres',
            user=user,
            password=password,
            host=host,
            port=port
        )
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {dbname}")
        print(f"Database '{dbname}' created successfully.")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database '{dbname}' already exists.")
    except Exception as e:
        print("Error creating database:", e)
    finally:
        cursor.close()
        connection.close()

       

# Create the database if it doesn't exist
# create_database(dbname, user, password, host, port)        


def execute_sql_file(sql_file, connection):
    # Open and read the SQL file
    with open(sql_file, 'r') as file:
        sql_script = file.read()

    # Split the SQL script into individual statements
    sql_commands = sql_script.split(';')
    # Remove empty statements and whitespace
    sql_commands_clean = [cmd.strip() for cmd in sql_commands if cmd.strip()]
    # print(sql_commands)

    # Disable autocommit to execute commands outside of a transaction
    connection.autocommit = True

    # Execute each SQL command
    try:
        cursor = connection.cursor()
        for cmd in sql_commands_clean:
            cursor.execute(cmd)
        connection.commit()
        print("SQL script executed successfully.")
    except Exception as e:
        connection.rollback()
        print("Error executing SQL script:", e)

def copy_data_to_postgres(dat_file, table_name, conn):
    try:
        cursor = conn.cursor()

        # Open the .dat file for reading
        with open(dat_file, 'r') as f:
            # Use psycopg2's copy_from method to copy data from the file to the table
            cursor.copy_from(f, table_name, sep='\t')

        # Commit the transaction
        conn.commit()
        print("Data copied from {} to {} table successfully.".format(dat_file, table_name))
    except Exception as e:
        # Rollback the transaction if an error occurs
        conn.rollback()
        print("Error copying data:", e)
    finally:
        # Close the cursor
        cursor.close()


# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname="recognition",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )
    print(f"Connected to the {os.getenv('dbname')} database.")
except Exception as e:
    print("Unable to connect to the database:", e)


# Path to your SQL file
sql_file_path = 'restore.sql'

# Execute the SQL file
# execute_sql_file(sql_file_path, connection)

# Copy data from .dat file to PostgreSQL table
# copy_data_to_postgres('4285.dat', 'fingerprints', connection)
# copy_data_to_postgres('4284.dat', 'songs', connection)

# Close the database connection
connection.close()
