import pandas as pd
import os
import logging

# Setup logging
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_cleaning.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DataCleaning:
    def __init__(self, csv_files):
        self.csv_files = csv_files
        self.dataframes = []
    
    def load_data(self):
        try:
            logging.info("Loading CSV files...")
            for file in self.csv_files:
                if os.path.exists(file):
                    df = pd.read_csv(file)
                    self.dataframes.append(df)
                    logging.info(f"Loaded {file}")
                else:
                    logging.warning(f"File {file} does not exist")
        except Exception as e:
            logging.error(f"Error loading CSV files: {e}")
            raise e

    def merge_the_data_frames(dataframes):
        logging.info("merging the whole data frames into one big data frame")
        try:
            return pd.concat(dataframes,ignore_index=True)
        except Exception as e:
            logging.error(f"error occured while merging the dataframes")
    
    def check_duplicates(self):
        try:
            logging.info("Checking for duplicates...")
            duplicates = self.merged_df.duplicated()
            if duplicates.any():
                logging.info(f"Found {duplicates.sum()} duplicate rows")
                self.merged_df = self.merged_df.drop_duplicates()
                logging.info("Duplicates removed")
            else:
                logging.info("No duplicates found")
        except Exception as e:
            logging.error(f"Error checking for duplicates: {e}")
            raise e

if __name__ == "__main__":
    csv_files = [
        'path/to/your/first.csv',
        'path/to/your/second.csv',
        'path/to/your/third.csv',
        'path/to/your/fourth.csv'
    ]

    data_cleaning = DataCleaning(csv_files)
    data_cleaning.load_data()
    data_cleaning.merge()
    data_cleaning.check_duplicates()

    # Save the cleaned data
    cleaned_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cleaned_data.csv")
    data_cleaning.merged_df.to_csv(cleaned_file_path, index=False)
    logging.info(f"Cleaned data saved to {cleaned_file_path}")
    print("Data cleaning process completed successfully.")
