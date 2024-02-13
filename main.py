import psycopg2

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

dbname="recognition"
user="postgres"
password="postgres"
host="127.0.0.1"
port="5432"        

# Create the database if it doesn't exist
# create_database(dbname, user, password, host, port)        


def execute_sql_file(sql_file, connection):
    # Open and read the SQL file
    with open(sql_file, 'r') as file:
        sql_script = file.read()

    # Split the SQL script into individual statements
    sql_commands = sql_script.split(';')

    # Remove empty statements and whitespace
    sql_commands = [cmd.strip() for cmd in sql_commands if cmd.strip()]

    # Disable autocommit to execute commands outside of a transaction
    connection.autocommit = True

    # Execute each SQL command
    # try:
    #     cursor = connection.cursor()
    #     for cmd in sql_commands[:-1]:
    #         cursor.execute(cmd)
    #     connection.commit()
    #     print("SQL script executed successfully.")
    # except Exception as e:
    #     connection.rollback()
    #     print("Error executing SQL script:", e)
    with open(sql_file,'r', encoding='utf-8') as f:
        for statement in f.readlines():    
            try:
                pg_cursor = connection.cursor()
                pg_cursor.execute(f'{statement.rstrip()}')
                connection.commit()
            except psycopg2.Error as errorMsg:
                print(errorMsg)        
                connection.rollback()


# Connect to the PostgreSQL database
try:
    connection = psycopg2.connect(
        dbname="recognition",
        user="postgres",
        password="postgres",
        host="127.0.0.1",
        port="5432"
    )
    print(f"Connected to the {dbname} database.")
except Exception as e:
    print("Unable to connect to the database:", e)

# Path to your SQL file
sql_file_path = 'restore.sql'

# Execute the SQL file
execute_sql_file(sql_file_path, connection)

# Close the database connection
connection.close()
