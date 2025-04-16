import sqlite3
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()


# This script loads the transformed CSV data into SQLite and Postgres database

def load_to_sqlite(transformed_csv = "output/transformed_students.csv", db_path="students.db"):
    df = pd.read_csv(transformed_csv)
    conn = sqlite3.connect(db_path)
    df.to_sql("students", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Loaded data into SQLite DB: {db_path}")


def load_to_postgres(csv_path):
    df = pd.read_csv(csv_path)

    db_url = os.getenv("POSTGRES_URL")
    engine = create_engine(db_url)

    df.to_sql("students", engine, if_exists="replace", index=False)
    print(f"Loaded data into PostgreSQL DB: {db_url}")

def main():
    csv_path = "output/transformed_students.csv"
    load_to_postgres(csv_path)
    load_to_sqlite(csv_path)



