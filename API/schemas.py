import os
import logging
from pydantic import BaseModel
from datetime import datetime

# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/schema.log"),
        logging.StreamHandler()
    ]
)

# Log schema creation start
logging.info("Starting schema definitions.")

# Define the schema for TelegramMessage
class TelegramMessageBase(BaseModel):
    channel_title: str
    channel_username: str
    message_id: int
    message: str
    message_date: datetime
    media_path: str
    emoji_used: str
    youtube_links: str

logging.info("Defined TelegramMessageBase schema.")

class TelegramMessageCreate(TelegramMessageBase):
    pass

logging.info("Defined TelegramMessageCreate schema.")

class TelegramMessage(TelegramMessageBase):
    id: int

    class Config:
        orm_mode = True

logging.info("Defined TelegramMessage schema.")

# Define the schema for DetectionResult
class DetectionResultBase(BaseModel):
    file_name: str
    class_id: int
    x_center: float
    y_center: float
    width: float
    height: float
    confidence: float

logging.info("Defined DetectionResultBase schema.")

class DetectionResultCreate(DetectionResultBase):
    pass

logging.info("Defined DetectionResultCreate schema.")

class DetectionResult(DetectionResultBase):
    id: int

    class Config:
        orm_mode = True

logging.info("Defined DetectionResult schema.")

# Log schema creation end
logging.info("Completed schema definitions.")
