import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection string (replace with your actual connection details)
DB_CONNECTION = os.environ["DB_CONNECTION"]


# Function to insert patient data into PostgreSQL
def insert_patient_data(first_name, last_name, age, date_value, weight, height, gender):
    """Function to insert patient data into PostgreSQL"""
    try:
        with psycopg2.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cursor:

                query = """
                INSERT INTO patients (first_name, last_name, age, date, weight, height, gender)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(query, (first_name, last_name, age, date_value, weight, height, gender))
                conn.commit()
                cursor.close()
                conn.close()

        return "Data saved successfully!"
    except Exception as e:
        return f"Error saving data: {e}"
