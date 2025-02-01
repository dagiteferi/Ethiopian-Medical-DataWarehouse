import torch
import cv2
from pathlib import Path
import logging
import pandas as pd

# Set up logging
logging.basicConfig(filename='detection.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

def setup_logging():
    logging.info('🚀 Starting object detection process.')

def log_info(message):
    logging.info(f'ℹ️ {message}')

def log_error(error):
    logging.error(f'❌ {error}')

def load_yolo_model():
    log_info('Loading YOLO model...')
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    log_info('YOLO model loaded successfully.')
    return model

def process_the_YOLO_object(path):
    logger.info("Processing the data collected from the YOLO object detection model...")
    output_data = []
    try:
        for filename in os.listdir(path):
            if filename.endswith('.txt'):
                filepath = os.path.join(path, filename)
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        data = line.strip().split()
                        class_id = int(data[0])
                        x_center = float(data[1])
                        y_center = float(data[2])
                        width = float(data[3])
                        height = float(data[4])
                        confidence = float(data[5])
                        output_data.append([filename, class_id, x_center, y_center, width, height, confidence])
       
        df = pd.DataFrame(output_data, columns=['filename', 'class_id', 'x_center', 'y_center', 'width', 'height', 'confidence'])
        df.to_csv('YOLO_output_data.csv', index=False)
        return df
    except Exception as e:
        logger.error(f"An error occurred while processing the data: {e}")

def main():
    setup_logging()
    
    try:
        model = load_yolo_model()
        detect_objects(model, 'path_to_your_scraped_images', 'detection_results', 'detection_results.csv')
        log_info('✅ Object detection process completed successfully.')
    except Exception as e:
        log_error(f'Error during object detection: {e}')

if __name__ == '__main__':
    main()
