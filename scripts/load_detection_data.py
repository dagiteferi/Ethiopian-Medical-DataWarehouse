import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Configure logging to write to file & display in Jupyter Notebook
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/detection_data_cleaning.log"),  # Log to file
        logging.StreamHandler()  # Log to Jupyter Notebook
    ]
)

# Load environment variables
load_dotenv("../.env")

DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
    """ Create and return database engine. """
    try:
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        print(f"DATABASE_URL: {DATABASE_URL}")  # Debugging: Print DATABASE_URL
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Test connection
        logging.info("Successfully connected to the PostgreSQL database.")
        return engine
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def create_table(engine):
    """ Create detection_results table if it does not exist. """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS detection_results (
        id SERIAL PRIMARY KEY,
        file_name TEXT,
        class_id INTEGER,
        x_center FLOAT,
        y_center FLOAT,
        width FLOAT,
        height FLOAT,
        confidence FLOAT
    );
    """
    try:
        with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as connection:
            connection.execute(text(create_table_query))
        logging.info("Table 'detection_results' created successfully.")
    except Exception as e:
        logging.error(f"Error creating table: {e}")
        raise

def insert_data(engine, cleaned_df):
    """ Inserts cleaned detection data into PostgreSQL database. """
    try:
        insert_query = """
        INSERT INTO detection_results 
        (file_name, class_id, x_center, y_center, width, height, confidence) 
        VALUES (:file_name, :class_id, :x_center, :y_center, :width, :height, :confidence)
        ON CONFLICT (file_name, class_id, x_center, y_center, width, height, confidence) DO NOTHING;
        """

        with engine.begin() as connection:  # Auto-commit enabled
            for _, row in cleaned_df.iterrows():
                # Debug log to ensure data is being inserted
                logging.info(f"Inserting: {row['file_name']} - {row['class_id']}")

                connection.execute(
                    text(insert_query),
                    {
                        "file_name": row["file_name"],
                        "class_id": row["class_id"],
                        "x_center": row["x_center"],
                        "y_center": row["y_center"],
                        "width": row["width"],
                        "height": row["height"],
                        "confidence": row["confidence"]
                    }
                )

        logging.info(f"{len(cleaned_df)} records inserted into PostgreSQL database.")
    except Exception as e:
        logging.error(f"Error inserting data: {e}")
        raise

