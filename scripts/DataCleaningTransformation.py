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

