# setup.py
# Auto-creates database on first run (for deployment)

import os
import sqlite3
import pandas as pd

def initialize():
    """Run this on every app start to ensure DB exists"""

    db_path = "database/urbaniq.db"
    csv_path = "data/raw/locations.csv"

    # Create folders if they don't exist
    os.makedirs("database", exist_ok=True)
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    # If DB already has data, skip
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            count = pd.read_sql(
                "SELECT COUNT(*) as c FROM locations_processed", conn
            ).iloc[0]["c"]
            conn.close()
            if count > 0:
                return  # Already initialized
        except:
            pass

    print("🔄 Initializing database...")

    # Run data pipeline
    from data.raw.enhanced_dataset import create_enhanced_dataset
    from database.db_setup import setup_database
    from data.processed.feature_engineering import feature_engineering

    create_enhanced_dataset()
    setup_database()
    feature_engineering()

    # Create users table
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

    print("✅ Database initialized!")

if __name__ == "__main__":
    initialize()