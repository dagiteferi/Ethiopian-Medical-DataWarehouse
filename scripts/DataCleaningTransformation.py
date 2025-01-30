import pandas as pd
import os
import logging
import re
import emoji

# Setup logging to file and console
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cleaning.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

class DataCleaning:
    def __init__(self):
        self.dataframes = []
    
    def load_data(self, path):
        logging.info("Loading the data")
        try:
            df = pd.read_csv(path)
            self.dataframes.append(df)
            return df
        except Exception as e:
            logging.error(f"Error occurred while loading the data: {e}")
            return None

    def merge(self, dataframes=None):
        try:
            logging.info("Merging dataframes...")
            if dataframes is None:
                dataframes = self.dataframes

            if len(dataframes) > 1:
                merged_df = pd.concat(dataframes, ignore_index=True)
                logging.info("Dataframes merged successfully")
            else:
                logging.warning("Not enough dataframes to merge")
                merged_df = dataframes[0]
            return merged_df
        except Exception as e:
            logging.error(f"Error merging dataframes: {e}")
            raise e
    
    def check_duplicates(self, df):
        try:
            logging.info("Checking for duplicates...")
            duplicates = df.duplicated()
            if duplicates.any():
                logging.info(f"Found {duplicates.sum()} duplicate rows")
            else:
                logging.info("No duplicates found")
            return duplicates
        except Exception as e:
            logging.error(f"Error checking for duplicates: {e}")
            raise e

    def handle_duplicates(self, df, duplicates):
        try:
            if duplicates.any():
                df = df.drop_duplicates()
                logging.info("Duplicates removed")
            return df
        except Exception as e:
            logging.error(f"Error handling duplicates: {e}")
            raise e
    
    def check_missing_values(self, df):
        try:
            logging.info("Checking for missing values...")
            missing_values = df.isnull().sum()
            total_missing = missing_values.sum()
            if total_missing > 0:
                logging.info(f"Found {total_missing} missing values")
            else:
                logging.info("No missing values found")
            return missing_values
        except Exception as e:
            logging.error(f"Error checking for missing values: {e}")
            raise e
    
    def handle_missing_values(self, df):
        try:
            logging.info("Handling missing values by dropping rows with missing values...")
            before_drop = df.shape[0]
            df = df.dropna()
            after_drop = df.shape[0]
            logging.info(f"Dropped {before_drop - after_drop} rows with missing values")
            return df
        except Exception as e:
            logging.error(f"Error handling missing values: {e}")
            raise e
    
    def extract_emojis(self, text):
        """Extract emojis from text, return 'No emoji' if none found."""
        emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
        return emojis if emojis else "No emoji"

    def extract_youtube_links(self, text):
        """Extract YouTube links from text, return 'No YouTube link' if none found."""
        youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
        links = re.findall(youtube_pattern, text)
        return ', '.join(links) if links else "No YouTube link"

    def remove_youtube_links(self, text):
        """Remove YouTube links from the message text."""
        youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
        return re.sub(youtube_pattern, '', text).strip()

    def clean_text(self, text):
        """Clean text by removing unwanted characters and normalizing."""
        text = self.remove_youtube_links(text)
        return text.strip()

    def clean_dataframe(self, df):
        """Perform all cleaning and standardization steps while avoiding SettingWithCopyWarning."""
        try:
            df = df.drop_duplicates(subset=["ID"]).copy()  # Ensure a new copy
            logging.info("Duplicates removed from dataset.")

            # Convert Date to datetime format, replacing NaT with None
            df.loc[:, 'Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df.loc[:, 'Date'] = df['Date'].where(df['Date'].notna(), None)
            logging.info("Date column formatted to datetime.")

            # Convert 'ID' to integer for PostgreSQL BIGINT compatibility
            df.loc[:, 'ID'] = pd.to_numeric(df['ID'], errors="coerce").fillna(0).astype(int)

            # Fill missing values
            df.loc[:, 'Message'] = df['Message'].fillna("No Message")
            df.loc[:, 'Media Path'] = df['Media Path'].fillna("No Media")
            logging.info("Missing values filled.")

            # Standardize text columns
            df.loc[:, 'Channel Title'] = df['Channel Title'].str.strip()
            df.loc[:, 'Channel Username'] = df['Channel Username'].str.strip()
            df.loc[:, 'Message'] = df['Message'].apply(self.clean_text)
            df.loc[:, 'Media Path'] = df['Media Path'].str.strip()
            logging.info("Text columns standardized.")

            # Extract emojis and store them in a new column
            df.loc[:, 'emoji_used'] = df['Message'].apply(self.extract_emojis)
            logging.info("Emojis extracted and stored in 'emoji_used' column.")
            
            # Extract YouTube links into a separate column
            df.loc[:, 'youtube_links'] = df['Message'].apply(self.extract_youtube_links)
            logging.info("YouTube links extracted and stored in 'youtube_links' column.")

            # Remove YouTube links from message text
            df.loc[:, 'Message'] = df['Message'].apply(self.remove_youtube_links)

            # Rename columns to match PostgreSQL schema
            df = df.rename(columns={
                "Channel Title": "channel_title",
                "Channel Username": "channel_username",
                "ID": "message_id",
                "Message": "message",
                "Date": "message_date",
                "Media Path": "media_path",
                "emoji_used": "emoji_used",
                "youtube_links": "youtube_links"
            })

            logging.info("Data cleaning completed successfully.")
            return df
        except Exception as e:
            logging.error(f"Data cleaning error: {e}")
            raise
    
    def save_cleaned_data(self, df, output_path):
        """Save cleaned data to a new CSV file."""
        try:
            df.to_csv(output_path, index=False)
            logging.info(f"Cleaned data saved successfully to '{output_path}'.")
            print(f"Cleaned data saved successfully to '{output_path}'.")
        except Exception as e:
            logging.error(f"Error saving cleaned data: {e}")
            raise

