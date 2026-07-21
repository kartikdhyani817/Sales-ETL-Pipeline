# Sales ETL Pipeline

An end-to-end Data Engineering project that demonstrates how raw sales data is extracted, validated, transformed, and loaded into a structured database using Python and MySQL.

> 🚧 This project is being developed incrementally over 10 days to simulate a real-world production ETL workflow.

---

## Project Overview

The Sales ETL Pipeline automates the process of handling sales data by:

- Extracting raw sales data from CSV files
- Validating data quality and schema
- Cleaning and transforming records
- Loading processed data into MySQL
- Generating logs for monitoring and debugging
- Creating a maintainable and modular ETL architecture

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
├── data/
│   ├── raw/
│   ├── processed/
│   └── archive/
├── logs/
├── output/
├── scripts/
│   ├── ingest.py
│   └── validate.py
├── sql/
├── utils/
│   └── logger.py
├── main.py
├── requirements.txt
└── README.md
```

---

## ETL Workflow

```
Raw CSV Data
      │
      ▼
Data Validation
      │
      ▼
Data Cleaning & Transformation
      │
      ▼
Processed Dataset
      │
      ▼
MySQL Database
      │
      ▼
SQL Analytics
```

---

## Current Progress

### ✅ Day 1

- Project structure created
- Virtual environment configured
- Required dependencies installed
- Sample sales dataset added
- Logging module implemented
- Data validation module created
- CSV ingestion pipeline completed

---

## Upcoming Features

- Data Cleaning
- Missing Value Handling
- Duplicate Removal
- Data Transformation
- MySQL Integration
- Incremental Loading
- SQL Reporting
- Data Quality Checks
- Error Handling
- Production Logging

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

Activate it (Windows):

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the project:

```bash
python main.py
```

---

## Learning Objectives

This project demonstrates practical Data Engineering concepts including:

- ETL Pipeline Design
- Data Validation
- Data Transformation
- Logging
- Python Project Structure
- Database Integration
- SQL
- Modular Programming

---

## Author

**Kartik Dhyani**

Aspiring Data Engineer | Python | SQL | Data Analytics | ETL Pipelines

---

## License

This project is created for learning and portfolio purposes.
