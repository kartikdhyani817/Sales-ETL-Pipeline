# Sales ETL Pipeline

An end-to-end Data Engineering project that demonstrates how raw sales data is extracted, validated, transformed, and loaded into a structured database using Python and MySQL.

> 🚧 This project is being built incrementally over 10 days to simulate a production-ready ETL workflow.

---

## Project Overview

The Sales ETL Pipeline automates the processing of retail sales data through a modular ETL architecture.

The pipeline performs:

- Extracting raw sales data from CSV files
- Validating data quality and schema
- Cleaning missing values
- Removing duplicate records
- Transforming and enriching data
- Generating data quality reports
- Saving processed data in Parquet format
- Preparing data for MySQL loading

---

## Tech Stack

- Python
- Pandas
- MySQL
- SQLAlchemy
- MySQL Connector
- PyArrow
- Python Dotenv
- VS Code

---

## Project Structure

```text
Sales_ETL_Pipeline/
│
├── config/
│   └── database.py
│
├── data/
│   ├── raw/
│   │   └── sales_data.csv
│   ├── processed/
│   │   └── clean_sales.parquet
│   └── archive/
│
├── logs/
│
├── output/
│
├── scripts/
│   ├── ingest.py
│   ├── validate.py
│   ├── clean.py
│   ├── report.py
│   ├── save.py
│   └── load_mysql.py
│
├── utils/
│   └── logger.py
│
├── sql/
│
├── main.py
├── requirements.txt
├── .gitignore
├── .env (local only)
└── README.md
```

---

## ETL Workflow

```
Raw CSV
    │
    ▼
Validation
    │
    ▼
Data Cleaning
    │
    ▼
Data Transformation
    │
    ▼
Quality Report
    │
    ▼
Parquet File
    │
    ▼
MySQL Database (In Progress)
```

---

## Features Implemented

### Day 1

- Project structure created
- Virtual environment configured
- Required dependencies installed
- CSV ingestion module developed
- Data validation module created
- Logging system implemented
- Modular ETL architecture established

---

### Day 2

- Duplicate record removal
- Missing value handling
- Data type conversion
- Feature engineering (`TotalAmount`)
- Data quality report generation
- Export cleaned data to Parquet
- Improved logging and modularization

---

### Day 3 (Current Progress)

- MySQL database integration initiated
- Environment variable configuration using `.env`
- SQLAlchemy database connection implemented
- MySQL loading module created
- Database connectivity under testing

> Final MySQL loading will be completed after database authentication is configured.

---

## Sample Dataset

The project processes retail sales records containing:

- Order ID
- Customer Name
- Product
- Category
- Quantity
- Price
- Order Date
- City

The pipeline automatically cleans and enriches the dataset before loading it into the database.

---

## Current Pipeline Output

The pipeline currently:

- Reads raw sales CSV
- Validates dataset structure
- Removes duplicate records
- Handles missing values
- Converts data types
- Generates TotalAmount column
- Produces a data quality report
- Saves processed data as Parquet
- Prepares data for database loading

---

## Upcoming Features

- Complete MySQL data loading
- Incremental loading
- SQL analytics queries
- Error handling improvements
- Configurable pipeline settings
- Scheduling support
- Automated reporting
- Performance optimization

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/<your-username>/Sales-ETL-Pipeline.git
```

Navigate to the project:

```bash
cd Sales-ETL-Pipeline
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment (Windows):

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the pipeline:

```bash
python main.py
```

---

## Learning Objectives

This project demonstrates practical Data Engineering concepts including:

- ETL Pipeline Design
- Data Validation
- Data Cleaning
- Data Transformation
- Feature Engineering
- Logging
- Modular Python Development
- SQLAlchemy
- MySQL Integration
- Environment Variable Management
- Production-style Project Structure

---

## Future Enhancements

- Airflow Scheduling
- Docker Deployment
- Cloud Storage Integration
- Data Warehouse Support
- Automated Monitoring
- Incremental ETL Processing

---

## Author

**Kartik Dhyani**

Aspiring Data Engineer | Python | SQL | Data Analytics | ETL Pipelines

---

## License

This project is licensed under the MIT License.
