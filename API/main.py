import os
import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from API import crud, models, schemas, database



# Ensure logs folder exists
os.makedirs("logs", exist_ok=True)

# Configure logging to write to file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/main.log"),
        logging.StreamHandler()
    ]
)

# Log application start
logging.info("Starting FastAPI application.")

# Create the database tables
models.Base.metadata.create_all(bind=database.engine)

# Initialize FastAPI application
app = FastAPI()

# Dependency to provide a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE endpoint for TelegramMessage
@app.post("/messages/", response_model=schemas.TelegramMessage)
def create_message(message: schemas.TelegramMessageCreate, db: Session = Depends(get_db)):
    logging.info(f"Received request to create message: {message}")
    return crud.create_message(db=db, message=message)

# READ endpoint for a single TelegramMessage
@app.get("/messages/{message_id}", response_model=schemas.TelegramMessage)
def read_message(message_id: int, db: Session = Depends(get_db)):
    logging.info(f"Received request to read message with ID: {message_id}")
    db_message = crud.get_message(db, message_id=message_id)
    if db_message is None:
        logging.warning(f"Message with ID: {message_id} not found")
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

# READ endpoint for multiple TelegramMessages
@app.get("/messages/", response_model=list[schemas.TelegramMessage])
def read_messages(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logging.info(f"Received request to read messages with skip: {skip} and limit: {limit}")
    messages = crud.get_messages(db, skip=skip, limit=limit)
    return messages

# UPDATE endpoint for TelegramMessage
@app.put("/messages/{message_id}", response_model=schemas.TelegramMessage)
def update_message(message_id: int, message: schemas.TelegramMessageCreate, db: Session = Depends(get_db)):
    logging.info(f"Received request to update message with ID: {message_id}")
    db_message = crud.update_message(db, message_id=message_id, updated_message=message)
    if db_message is None:
        logging.warning(f"Message with ID: {message_id} not found")
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

# DELETE endpoint for TelegramMessage
@app.delete("/messages/{message_id}", response_model=schemas.TelegramMessage)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    logging.info(f"Received request to delete message with ID: {message_id}")
    db_message = crud.delete_message(db, message_id=message_id)
    if db_message is None:
        logging.warning(f"Message with ID: {message_id} not found")
        raise HTTPException(status_code=404, detail="Message not found")
    return db_message

# Log application ready
logging.info("FastAPI application is ready.")
