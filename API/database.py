import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database connection information from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT")

# Define the Database URL using environment variables
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# Create the engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create the session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/api_database_connection.log"),
        logging.StreamHandler()
    ]
)

# Dependency to provide a database session
def get_db():
    db = SessionLocal()
    try:
        logging.info("Database session created.")
        yield db
    except Exception as e:
        logging.error(f"Error during database session: {e}")
        raise
    finally:
        db.close()
        logging.info("Database session closed.")

# Log the creation of the engine
logging.info("Database engine created.")
