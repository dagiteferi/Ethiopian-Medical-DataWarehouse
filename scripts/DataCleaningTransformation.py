import pandas as pd
import os
import logging

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
    
    def load_data(self, file_path):
        try:
            logging.info(f"Loading CSV file: {file_path}")
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)
                self.dataframes.append(df)
                logging.info(f"Loaded {file_path}")
            else:
                logging.warning(f"File {file_path} does not exist")
        except Exception as e:
            logging.error(f"Error loading CSV file {file_path}: {e}")
            raise e

    def merge(self):
        try:
            logging.info("Merging dataframes...")
            if len(self.dataframes) > 1:
                merged_df = pd.concat(self.dataframes, ignore_index=True)
                logging.info("Dataframes merged successfully")
            else:
                logging.warning("Not enough dataframes to merge")
                merged_df = self.dataframes[0]
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
                df = df.drop_duplicates()
                logging.info("Duplicates removed")
            else:
                logging.info("No duplicates found")
            return df
        except Exception as e:
            logging.error(f"Error checking for duplicates: {e}")
            raise e


