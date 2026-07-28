# 📊 Sales ETL Pipeline

An end-to-end Data Engineering project that automates the complete ETL (Extract, Transform, Load) workflow using Python, MySQL, SQLAlchemy, Pandas and Streamlit.

The project ingests raw sales data, validates and cleans it, performs feature engineering, stores processed data in MySQL, generates business reports, creates visual analytics, and provides an interactive dashboard for business users.

---

# 🚀 Features

- CSV Data Ingestion
- Data Validation
- Data Cleaning
- Feature Engineering
- Parquet Export
- MySQL Integration
- SQL Analytics
- Business Report Generation
- Interactive Streamlit Dashboard
- KPI Monitoring
- Advanced Data Filtering
- Searchable Sales Database
- Download Center
- Data Visualization

---

# 🏗️ Project Architecture

```
Raw CSV
    │
    ▼
Validation
    │
    ▼
Cleaning
    │
    ▼
Feature Engineering
    │
    ▼
Parquet Export
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
Interactive Dashboard
```

---

# 📂 Project Structure

```
Sales_ETL_Pipeline/

├── app.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── config/
│   └── database.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── archive/
│
├── logs/
│
├── output/
│   ├── business_report.txt
│   └── charts/
│
├── scripts/
│   ├── ingest.py
│   ├── validate.py
│   ├── clean.py
│   ├── save.py
│   ├── load_mysql.py
│   ├── analytics.py
│   ├── business_report.py
│   ├── charts.py
│   └── report.py
│
└── utils/
    └── logger.py
```

---

# ⚙️ Technologies Used

- Python
- Pandas
- MySQL
- SQLAlchemy
- MySQL Connector
- PyArrow
- Streamlit
- Matplotlib

---

# 📈 Dashboard Features

- KPI Cards
- Revenue Analysis
- Category Analytics
- City Analytics
- Product Analytics
- Monthly Revenue Trend
- Interactive Filters
- Searchable Sales Database
- Business Report Viewer
- Download Centre

---

# 📊 Business Analytics

The project calculates:

- Total Revenue
- Total Orders
- Average Order Value
- Revenue by Category
- Revenue by City
- Monthly Sales Trend
- Top Selling Products

---

# ▶️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/Sales-ETL-Pipeline.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create MySQL database

```sql
CREATE DATABASE sales_etl;
```




Run ETL Pipeline

```bash
python main.py
```

Launch Dashboard

```bash
streamlit run app.py
```

---


# 📌 Future Improvements

- Apache Airflow Scheduling
- Docker Support
- CI/CD using GitHub Actions
- Unit Testing
- AWS Deployment
- Azure Data Factory Integration
- Snowflake Support
- Power BI Integration

---

# 👨‍💻 Author

**Kartik Dhyani**

GitHub:
https://github.com/kartikdhyani817
