from telethon import TelegramClient
import csv
import os
import logging
import json
from dotenv import load_dotenv

# 🔹 Set up Logging
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scraping.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 🔹 Load environment variables
load_dotenv()
try:
    api_id = int(os.getenv("TG_API_ID"))
    api_hash = os.getenv("TG_API_HASH")
    phone = os.getenv("phone")

    if not api_id or not api_hash or not phone:
        raise ValueError("Missing TG_API_ID, TG_API_HASH, or phone in .env file")

except Exception as e:
    logging.error(f"Error loading .env variables: {e}")
    raise SystemExit(f"❌ ERROR: {e}")

# 🔹 Get absolute paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Root folder
CHANNELS_FILE = os.path.join(ROOT_DIR, "channels.json")
DATA_DIR = os.path.join(ROOT_DIR, "data")
MEDIA_DIR = os.path.join(ROOT_DIR, "photos")

# 🔹 Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(MEDIA_DIR, exist_ok=True)

# 🔹 Function to load channels from JSON
def load_channels_from_json(file_path):
    try:
        if not os.path.exists(file_path):
            logging.error(f"❌ ERROR: {file_path} not found!")
            return [], []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("channels", []), data.get("comments", [])
    except Exception as e:
        logging.error(f"Error reading channels from JSON: {e}")
        return [], []

# 🔹 Function to scrape data from a single channel
async def scrape_channel(client, channel_username, writer, media_dir, num_messages):
    try:
        logging.info(f"Fetching entity for: {channel_username}")
        entity = await client.get_entity(channel_username)
        channel_title = entity.title
        message_count = 0

        async for message in client.iter_messages(entity, limit=num_messages):
            media_path = None
            if message.media:
                file_extension = "jpg"
                if hasattr(message.media, "document"):
                    file_extension = message.media.document.mime_type.split("/")[-1]

                filename = f"{channel_username}_{message.id}.{file_extension}"
                media_path = os.path.join(media_dir, filename)
                await client.download_media(message.media, media_path)
                logging.info(f"Downloaded media for message ID {message.id}")

            writer.writerow([channel_title, channel_username, message.id, message.message, message.date, media_path])
            logging.info(f"Processed message ID {message.id} from {channel_username}")

            message_count += 1
        
        if message_count == 0:
            logging.info(f"No messages found for {channel_username}")

    except Exception as e:
        logging.error(f"Error scraping {channel_username}: {e}")

# 🔹 Initialize the Telegram Client
client = TelegramClient("scraping_session", api_id, api_hash)

async def main():
    try:
        print("🔄 Starting Telegram Client...")
        await client.start(phone)
        print("✅ Client started successfully.")

        # Load channels from JSON
        channels, comments = load_channels_from_json(CHANNELS_FILE)
        print(f"📌 Channels loaded: {channels}")

        if not channels:
            print("❌ No channels found to scrape.")
            return

        num_messages_to_scrape = 4000  # Number of messages to scrape

        for channel in channels:
            print(f"📥 Processing channel: {channel}")

            csv_filename = os.path.join(DATA_DIR, f"{channel[1:]}_data.csv")  # Remove '@' from channel name
            with open(csv_filename, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Channel Title", "Channel Username", "ID", "Message", "Date", "Media Path"])

                await scrape_channel(client, channel, writer, MEDIA_DIR, num_messages_to_scrape)
                print(f"✅ Scraped data from {channel}.")

        # Log commented channels if needed
        if comments:
            print(f"📝 Commented channels: {', '.join(comments)}")

    except Exception as e:
        logging.error(f"Error in main function: {e}")
        print(f"❌ Error in main function: {e}")
    finally:
        await client.disconnect()
        print("🔴 Disconnected from Telegram.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
