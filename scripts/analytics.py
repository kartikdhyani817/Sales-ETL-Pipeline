import pandas as pd
from sqlalchemy import text

from config.database import engine


def run_analytics():

    queries = {

        "Total Sales": """
        SELECT SUM(TotalAmount) AS value
        FROM sales;
        """,

        "Total Orders": """
        SELECT COUNT(*) AS value
        FROM sales;
        """,

        "Average Order Value": """
        SELECT ROUND(AVG(TotalAmount),2) AS value
        FROM sales;
        """,

        "Top Selling Product": """
        SELECT Product,
               SUM(Quantity) AS TotalSold
        FROM sales
        GROUP BY Product
        ORDER BY TotalSold DESC
        LIMIT 1;
        """,

        "Sales By Category": """
        SELECT Category,
               SUM(TotalAmount) AS Revenue
        FROM sales
        GROUP BY Category;
        """,

        "Sales By City": """
        SELECT City,
               SUM(TotalAmount) AS Revenue
        FROM sales
        GROUP BY City
        ORDER BY Revenue DESC;
        """
    }

    results = {}

    with engine.connect() as connection:

        for title, query in queries.items():

            df = pd.read_sql(text(query), connection)

            results[title] = df

    return results