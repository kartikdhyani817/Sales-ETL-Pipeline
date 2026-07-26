# Sales ETL Pipeline

An end-to-end Data Engineering project that demonstrates how raw sales data is extracted, validated, transformed, loaded into MySQL, analyzed using SQL, and visualized through automated charts.

> 🚀 A production-style ETL pipeline built using Python, Pandas, MySQL, SQLAlchemy, SQL, and Matplotlib.

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
- Generate automated business reports
- Create visual analytics dashboards

---

# Tech Stack

- Python
- Pandas
- MySQL
- SQLAlchemy
- MySQL Connector
- SQL
- PyArrow
- Matplotlib
- Python Dotenv
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
│   ├── business_report.txt
│   └── charts/
│       ├── Dashboard.png
│       ├── Monthly_Sales.png
│       ├── Revenue_Category.png
│       ├── Revenue_City.png
│       └── Top_Products.png
│
├── scripts/
│   ├── analytics.py
│   ├── business_report.py
│   ├── charts.py
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
    │
    ▼
Charts & Dashboard
```

---

# Features Implemented

## Day 1

- Project setup
- CSV ingestion
- Data validation
- Logging system
- Modular ETL architecture

---

## Day 2

- Duplicate removal
- Missing value handling
- Data type conversion
- Feature engineering
- Data quality reporting
- Export to Parquet

---

## Day 3

- MySQL integration
- SQLAlchemy connection
- Environment variable management
- Automatic table creation
- Load transformed data into MySQL

---

## Day 4

- SQL analytics module
- Business KPI generation
- Automated business report
- Revenue analysis
- Category analysis
- City analysis
- Product analysis

---

## Day 5

- Automated chart generation
- Revenue by category visualization
- Revenue by city visualization
- Top-selling products chart
- Monthly revenue trend analysis
- Dashboard summary generation
- Automatic chart export as PNG files

---

# Business Analytics Generated

The pipeline automatically calculates:

- Total Sales
- Total Orders
- Average Order Value
- Top Selling Product
- Revenue by Category
- Revenue by City
- Monthly Revenue Trend

---

# Visual Analytics Generated

The pipeline automatically creates the following charts:

- Revenue by Category
- Revenue by City
- Top 5 Selling Products
- Monthly Sales Trend
- Dashboard Summary

All charts are saved automatically inside the `output/charts/` directory.

---

# Output Files

## Processed Dataset

```
data/processed/clean_sales.parquet
```

## Business Report

```
output/business_report.txt
```

## Dashboard Charts

```
output/charts/

Dashboard.png

Monthly_Sales.png

Revenue_Category.png

Revenue_City.png

Top_Products.png
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

# Data Visualization

The project uses **Matplotlib** to generate automated business charts directly from SQL query results, making it easy to visualize key performance indicators and sales trends without manual intervention.

---

# Learning Objectives

This project demonstrates practical Data Engineering concepts including:

- ETL Pipeline Development
- Data Cleaning
- Data Validation
- Feature Engineering
- SQL Analytics
- MySQL Integration
- SQLAlchemy
- Automated Reporting
- Data Visualization
- Business KPI Analysis
- Logging
- Modular Python Development
- Production-style Project Structure

---

# Future Enhancements

- Interactive Streamlit Dashboard
- Incremental ETL Loading
- Airflow Scheduling
- Docker Deployment
- Cloud Storage Integration
- Data Warehouse Support
- Email Report Automation
- Monitoring & Alerting

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

Configure the `.env` file with your MySQL credentials.

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
