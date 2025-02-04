# models.py
import os
import logging
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from API.database import Base


# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/model.log"),
        logging.StreamHandler()
    ]
)

# Log model creation start
logging.info("Starting model definitions.")

# Define the TelegramMessage model
class TelegramMessage(Base):
    __tablename__ = "telegram_messages"

    id = Column(Integer, primary_key=True, index=True)
    channel_title = Column(String, index=True)
    channel_username = Column(String, index=True)
    message_id = Column(Integer, unique=True, index=True)
    message = Column(Text)
    message_date = Column(DateTime)
    media_path = Column(String)
    emoji_used = Column(String)
    youtube_links = Column(String)

    # Log the definition of the model
    logging.info("Defined TelegramMessage model.")

# Define the DetectionResult model
class DetectionResult(Base):
    __tablename__ = "detection_results"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    class_id = Column(Integer, index=True)
    x_center = Column(Float)
    y_center = Column(Float)
    width = Column(Float)
    height = Column(Float)
    confidence = Column(Float)

    # Log the definition of the model
    logging.info("Defined DetectionResult model.")

# Log model creation end
logging.info("Completed model definitions.")
