# database/db_setup.py
# Creates our SQLite database and loads the location data into it

import sqlite3
import pandas as pd
import os

def setup_database():
    # Load the CSV we just created
    df = pd.read_csv("data/raw/locations.csv")

    # Connect to SQLite (creates the file if it doesn't exist)
    conn = sqlite3.connect("database/urbaniq.db")
    cursor = conn.cursor()

    # Drop table if exists (so we can re-run safely)
    cursor.execute("DROP TABLE IF EXISTS locations")

    # Create the locations table
    cursor.execute("""
        CREATE TABLE locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area TEXT NOT NULL,
            city TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            population_density INTEGER,
            avg_income INTEGER,
            avg_rent INTEGER,
            metro_distance_km REAL,
            hospitals_nearby INTEGER,
            schools_nearby INTEGER,
            competition_score REAL,
            office_density REAL,
            growth_rate REAL,
            sentiment_score REAL
        )
    """)

    # Insert all rows from dataframe into database
    df.to_sql("locations", conn, if_exists="replace", index=False)

    # Verify it worked
    result = pd.read_sql("SELECT * FROM locations LIMIT 5", conn)
    print("✅ Database created successfully!")
    print(f"✅ Total areas loaded: {len(df)}")
    print(result[["area", "city", "avg_rent", "competition_score"]])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()