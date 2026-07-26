import os
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text

from config.database import engine


def generate_charts():

    os.makedirs("output/charts", exist_ok=True)

    with engine.connect() as connection:

        # Revenue by Category
        category = pd.read_sql(text("""
            SELECT Category,
                   SUM(TotalAmount) AS Revenue
            FROM sales
            GROUP BY Category
            ORDER BY Revenue DESC;
        """), connection)

        plt.figure(figsize=(8,5))
        plt.bar(category["Category"], category["Revenue"])
        plt.title("Revenue by Category")
        plt.xlabel("Category")
        plt.ylabel("Revenue")
        plt.tight_layout()
        plt.savefig("output/charts/Revenue_Category.png")
        plt.close()


        # Revenue by City
        city = pd.read_sql(text("""
            SELECT City,
                   SUM(TotalAmount) AS Revenue
            FROM sales
            GROUP BY City
            ORDER BY Revenue DESC;
        """), connection)

        plt.figure(figsize=(8,5))
        plt.bar(city["City"], city["Revenue"])
        plt.title("Revenue by City")
        plt.xlabel("City")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("output/charts/Revenue_City.png")
        plt.close()


        # Top Products
        product = pd.read_sql(text("""
            SELECT Product,
                   SUM(Quantity) AS Sold
            FROM sales
            GROUP BY Product
            ORDER BY Sold DESC
            LIMIT 5;
        """), connection)

        plt.figure(figsize=(8,5))
        plt.bar(product["Product"], product["Sold"])
        plt.title("Top 5 Products")
        plt.xlabel("Product")
        plt.ylabel("Units Sold")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("output/charts/Top_Products.png")
        plt.close()


        # Monthly Revenue
        monthly = pd.read_sql(text("""
            SELECT DATE_FORMAT(OrderDate,'%Y-%m') AS Month,
                   SUM(TotalAmount) AS Revenue
            FROM sales
            GROUP BY Month
            ORDER BY Month;
        """), connection)

        plt.figure(figsize=(8,5))
        plt.plot(monthly["Month"], monthly["Revenue"], marker="o")
        plt.title("Monthly Revenue")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("output/charts/Monthly_Sales.png")
        plt.close()


        # Dashboard KPI
        total_sales = pd.read_sql(
            text("SELECT SUM(TotalAmount) AS value FROM sales;"),
            connection
        ).iloc[0,0]

        total_orders = pd.read_sql(
            text("SELECT COUNT(*) AS value FROM sales;"),
            connection
        ).iloc[0,0]

        avg_order = pd.read_sql(
            text("SELECT AVG(TotalAmount) AS value FROM sales;"),
            connection
        ).iloc[0,0]

        top_product = pd.read_sql(text("""
            SELECT Product
            FROM sales
            GROUP BY Product
            ORDER BY SUM(Quantity) DESC
            LIMIT 1;
        """), connection).iloc[0,0]

        plt.figure(figsize=(8,5))

        plt.axis("off")

        plt.text(0.05,0.85,f"Total Sales : ₹{total_sales:,.2f}",fontsize=14)

        plt.text(0.05,0.65,f"Total Orders : {total_orders}",fontsize=14)

        plt.text(0.05,0.45,f"Average Order Value : ₹{avg_order:,.2f}",fontsize=14)

        plt.text(0.05,0.25,f"Top Product : {top_product}",fontsize=14)

        plt.title("Sales Dashboard Summary",fontsize=18)

        plt.savefig("output/charts/Dashboard.png")

        plt.close()

    print("\nCharts generated successfully.")