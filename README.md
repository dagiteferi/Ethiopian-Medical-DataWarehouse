# Telegram-Ethiopian-Medical-channel-data-warehouse

## Table of Contents
- [Overview](#overview)
- [Technologies](#technologies)
- [Folder Organization](#folder-organization)
- [Setup](#setup)
- [Notes](#notes)
- [Contributing](#contributing)


## Overview
### Project Overview
This project aims to build a data warehouse to store data on Ethiopian medical businesses scraped from the web and Telegram channels. The data warehouse will enable comprehensive analysis, identification of trends, and efficient querying and reporting. Additionally, the project integrates object detection capabilities using YOLO (You Only Look Once) to enhance data analysis
### Business Need
A centralized data warehouse allows for efficient and effective data analysis. By consolidating fragmented data, we can uncover valuable insights about Ethiopian medical businesses, leading to informed decision-making.

### Key Features
### Data Scraping and Collection Pipeline

- Extract data from relevant Telegram channels.
- Collect images for object detection.
- Store raw data in a temporary location..

### Data Cleaning and Transformation

- Remove duplicates, handle missing values, standardize formats, and validate data.
- Store cleaned data in a database.
- Transform data using DBT (Data Build Tool).

### Object Detection Using YOLO

- Set up the environment and download the YOLO model.
- Detect objects in images.
- Store detection data in a database table.

### Data Exposure Using FastAPI

- Set up a FastAPI application.
- Configure database connection.
- Define data models and schemas.
- Implement CRUD operations.
- Create API endpoints.

## Technologies
- Telethon
- PostgreSQL
- YOLO (You Only Look Once)
- FastAPI
- DBT(Data Build Tool)
- Python

## Folder Organization
 ```bash
   Directory structure:
└── Ethiopian-medical-datawarehouse
    ├── requirements.txt
    ├── yolov5s.pt
    ├── API/
    │   ├── crud.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   ├── schemas.py
    │   ├── frontEnd/
    │   │   ├── index.html
    │   │   ├── script.js
    │   │   └── style.css
    ├── data_house/
    │   ├── dbt_project.yml
    │   ├── .gitignore
    │   ├── analyses/
    │   │   └── .gitkeep
    │   ├── logs/
    │   ├── macros/
    │   │   └── .gitkeep
    │   ├── models/
    │   │   ├── example/
    │   │   │   ├── my_first_dbt_model.sql
    │   │   │   ├── my_second_dbt_model.sql
    │   │   │   ├── schema.yml
    │   │   │   └── transform_messages.sql
    │   │   └── sources/
    │   │       └── sources.yml
    │   ├── seeds/
    │   │   └── .gitkeep
    │   ├── snapshots/
    │   │   └── .gitkeep
    │   │   ├── compiled/
    │   │   │   └── data_house/
    │   │   │       └── models/
    │   │   │           └── example/
    │   │   │               ├── my_first_dbt_model.sql
    │   │   │               ├── my_second_dbt_model.sql
    │   │   │               ├── transform_messages.sql  
    ├── notebooks/
    │   ├── README.md
    │   ├── DataCleaningTransformation.ipynb
    │   ├── YOLO.ipynb
    │   ├── __init__.py
    │   └── detection_data_cleaning_load.ipynb
    ├── scripts/
    │   ├── README.md
    │   ├── DataCleaningTransformation.py
    │   ├── __init__.py
    │   ├── database.py
    │   ├── detection_data_cleaning.py
    │   ├── load_detection_data.py
    │   ├── yolo_object_detection.py
    ├── src/
    │   ├── __init__.py
    │   ├── file_structure.py
    │   └── scraper.py
    ├── tests/
    │   └── __init__.py
    └── .github/
        └── workflows/
            └── unittests.yml

```


## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/dagiteferi/Telegram-Ethiopian-Medical-channel-data-warehouse.git
   cd Telegram-Ethiopian-Medical-channel-data-warehouse
```
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. change directory to run the AIP locally.
```bash
   cd src
```
## Notes
- Ensure you have all the necessary API keys and access tokens for Telegram.
- Follow the instructions in the requirements.txt file to install all dependencies.

## Contributing
Fork the repository.
Create your feature branch 
```bash
(git checkout -b feature/AmazingFeature).
```
Commit your changes 
```bash
(git commit -m 'Add some AmazingFeature')
```
Push to the branch 
```bash
(git push origin feature/AmazingFeature).
```





Open a Pull Request.
