import psycopg2
import os
import io
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL connection parameters
dbname = os.getenv('dbname')
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')



# Path to your SQL file
sql_file_path = 'recognition_results.sql'

try:
    connection = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = connection.cursor()
    print(f"Connected to the {dbname} database.")
    print("Database connection established.")
    
    # Read and execute the SQL file
    with open(sql_file_path, 'r') as file:
        sql_commands = file.read()
    
    # Split the SQL commands
    sql_commands = sql_commands.split(';')
    sql_clean_commands = [ cmd.strip() for cmd in sql_commands]
    data =sql_clean_commands[17].strip()
    df = pd.DataFrame(data)
    df.to_csv('sql_clean_data.csv', index=False)
    print("WHAT "*5)
    

    # # loop through the clean SQL commands
    # for command in sql_clean_commands:
    #     if command.strip():
    #         if command.strip().upper().startswith('COPY'):
    #             # Handle COPY commands separately
    #              cursor.copy_expert(command, io.StringIO(data))
    #         else:
    #             # Execute other commands normally
    #             cursor.execute(command)
    
    connection.commit()
    print("SQL file executed successfully.")

except Exception as error:
    print(f"Error: {error}")
finally:
    # Close the database connection
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")




























# def create_database(dbname, user, password, host, port):
#     try:
#         connection = psycopg2.connect(
#             dbname='postgres',
#             user=user,
#             password=password,
#             host=host,
#             port=port
#         )
#         connection.autocommit = True
#         cursor = connection.cursor()
#         cursor.execute(f"CREATE DATABASE {dbname}")
#         print(f"Database '{dbname}' created successfully.")
#     except psycopg2.errors.DuplicateDatabase:
#         print(f"Database '{dbname}' already exists.")
#     except Exception as e:
#         print("Error creating database:", e)
#     finally:
#         cursor.close()
#         connection.close()

# Create the database if it doesn't exist
# create_database(dbname, user, password, host, port) 




# def execute_sql_file(sql_file, connection):
#     # Open and read the SQL file
#     with open(sql_file, 'r') as file:
#         sql_script = file.read()

#     # Split the SQL script into individual statements
#     sql_commands = sql_script.split(';')
#     # Remove empty statements and whitespace
#     sql_commands_clean = [cmd.strip() for cmd in sql_commands if cmd.strip()]
#     # print(sql_commands)

#     # Disable autocommit to execute commands outside of a transaction
#     connection.autocommit = True

#     # Execute each SQL command
#     try:
#         cursor = connection.cursor()
#         for cmd in sql_commands_clean:
#             print("SOMETHING"*5)
#             print(cmd)
#             cursor.execute(cmd)
#         connection.commit()
#         print("SQL script executed successfully.")
#     except Exception as e:
#         connection.rollback()
#         print("Error executing SQL script:", e)



# # Connect to the PostgreSQL database
# try:
#     connection = psycopg2.connect(
#         dbname="recognition",
#         user="postgres",
#         password="postgres",
#         host="127.0.0.1",
#         port="5432"
#     )
#     print(f"Connected to the {os.getenv('dbname')} database.")
# except Exception as e:
#     print("Unable to connect to the database:", e)


# # Path to your SQL file
# sql_file_path = 'recognition_results.sql'

# # Execute the SQL file
# execute_sql_file(sql_file_path, connection)

# # Close the database connection
# except Exception as error:
#     print(f"Error: {error}")
# finally:
#     # Close the database connection
#     if cursor:
#         cursor.close()
#     if connection:
#         connection.close()
#     print("Database connection closed.")