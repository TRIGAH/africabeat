import os
import psycopg2
import io
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def get_connection(dbname,user,password,host,port):
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

    except Exception as error:
        print(f"Error: {error}")

    return cursor