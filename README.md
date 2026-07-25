# Sales ETL Pipeline

An end-to-end Data Engineering project that demonstrates how raw sales data is extracted, validated, transformed, loaded into MySQL, and analyzed using SQL to generate automated business reports.

> 🚀 Built as a hands-on Data Engineering portfolio project using Python, Pandas, MySQL, SQLAlchemy, and SQL Analytics.

---

# Project Overview

The Sales ETL Pipeline automates the complete lifecycle of sales data processing.

The pipeline performs:

- Extract raw sales data
- Validate dataset structure
- Clean missing values
- Remove duplicate records
- Transform and enrich data
- Generate data quality reports
- Save processed data as Parquet
- Load cleaned data into MySQL
- Execute SQL analytics
- Generate an automated business report

---

# Tech Stack

- Python
- Pandas
- MySQL
- SQLAlchemy
- MySQL Connector
- PyArrow
- Python Dotenv
- SQL
- VS Code

---

# Project Structure

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
│   └── business_report.txt
│
├── scripts/
│   ├── analytics.py
│   ├── business_report.py
│   ├── clean.py
│   ├── ingest.py
│   ├── load_mysql.py
│   ├── report.py
│   ├── save.py
│   └── validate.py
│
├── sql/
│
├── utils/
│   └── logger.py
│
├── .env
├── .gitignore
├── main.py
├── requirements.txt
└── README.md
```

---

# ETL + Analytics Workflow

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
Transformation
    │
    ▼
Quality Report
    │
    ▼
Parquet File
    │
    ▼
MySQL Database
    │
    ▼
SQL Analytics
    │
    ▼
Business Report
```

---

# Features Implemented

## Day 1

- Modular project structure
- CSV ingestion
- Data validation
- Logging
- Modular ETL architecture

---

## Day 2

- Duplicate removal
- Missing value handling
- Data type conversion
- Feature engineering
- Parquet export
- Data quality reporting

---

## Day 3

- MySQL integration
- SQLAlchemy database connection
- Environment variable management
- Automatic table creation
- Load cleaned data into MySQL

---

## Day 4

- SQL analytics module
- Business KPI generation
- Automated business report
- Revenue analysis
- Product performance analysis
- Category-wise sales analysis
- City-wise sales analysis

---

# Business Analytics Generated

The pipeline automatically calculates:

- Total Sales
- Total Orders
- Average Order Value
- Top Selling Product
- Revenue by Category
- Revenue by City

These insights are generated directly from the MySQL database using SQL queries.

---

# Output Files

### Processed Dataset

```
data/processed/clean_sales.parquet
```

### Business Report

```
output/business_report.txt
```

---

# SQL Concepts Used

- SELECT
- SUM()
- AVG()
- COUNT()
- GROUP BY
- ORDER BY
- LIMIT
- Aggregate Functions

---

# Learning Objectives

This project demonstrates practical Data Engineering concepts including:

- ETL Pipeline Development
- Data Cleaning
- Feature Engineering
- Data Validation
- Logging
- SQLAlchemy
- MySQL Integration
- SQL Analytics
- Business KPI Reporting
- Modular Python Development
- Production-style Project Structure

---

# Future Enhancements

- Interactive Dashboards
- Data Visualization using Matplotlib
- Incremental ETL Loading
- Airflow Scheduling
- Docker Deployment
- Cloud Storage Integration
- Data Warehouse Support
- Automated Monitoring
- Email Report Delivery

---

# How to Run

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

Configure your `.env` file with MySQL credentials.

Run the pipeline:

```bash
python main.py
```

---

# Author

**Kartik Dhyani**

Aspiring Data Engineer | Python | SQL | Data Analytics | ETL Pipelines

---

# License

This project is licensed under the MIT License.
