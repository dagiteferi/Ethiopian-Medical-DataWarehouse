import os
import logging
from sqlalchemy.orm import Session
from API import models, schemas


# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/crud.log"),
        logging.StreamHandler()
    ]
)

# Log CRUD operation start
logging.info("Starting CRUD operations definitions.")

# CREATE operation for TelegramMessage
def create_message(db: Session, message: schemas.TelegramMessageCreate):
    db_message = models.TelegramMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    logging.info(f"Created message with ID: {db_message.id}")
    return db_message

# READ operation for a single TelegramMessage
def get_message(db: Session, message_id: int):
    db_message = db.query(models.TelegramMessage).filter(models.TelegramMessage.message_id == message_id).first()
    if db_message:
        logging.info(f"Retrieved message with ID: {db_message.id}")
    else:
        logging.warning(f"Message with ID: {message_id} not found")
    return db_message

# READ operation for multiple TelegramMessages
def get_messages(db: Session, skip: int = 0, limit: int = 10):
    messages = db.query(models.TelegramMessage).offset(skip).limit(limit).all()
    logging.info(f"Retrieved {len(messages)} messages")
    return messages

# UPDATE operation for TelegramMessage
def update_message(db: Session, message_id: int, updated_message: schemas.TelegramMessageCreate):
    db_message = db.query(models.TelegramMessage).filter(models.TelegramMessage.message_id == message_id).first()
    if db_message:
        for key, value in updated_message.dict().items():
            setattr(db_message, key, value)
        db.commit()
        db.refresh(db_message)
        logging.info(f"Updated message with ID: {db_message.id}")
    else:
        logging.warning(f"Message with ID: {message_id} not found")
    return db_message

# DELETE operation for TelegramMessage
def delete_message(db: Session, message_id: int):
    db_message = db.query(models.TelegramMessage).filter(models.TelegramMessage.message_id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        logging.info(f"Deleted message with ID: {db_message.id}")
    else:
        logging.warning(f"Message with ID: {message_id} not found")
    return db_message

# Log CRUD operation end
logging.info("Completed CRUD operations definitions.")
