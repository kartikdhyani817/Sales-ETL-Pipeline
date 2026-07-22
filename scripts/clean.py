import pandas as pd
from utils.logger import logger


def clean_data(df):

    logger.info("Cleaning started")

    initial_rows = len(df)

    # Remove duplicate rows
    df = df.drop_duplicates()

    duplicates_removed = initial_rows - len(df)

    # Fill missing city values
    df["City"] = df["City"].fillna("Unknown")

    # Fill missing quantity
    df["Quantity"] = df["Quantity"].fillna(1)

    # Convert data types
    df["Quantity"] = df["Quantity"].astype(int)

    df["Price"] = df["Price"].astype(float)

    df["OrderDate"] = pd.to_datetime(df["OrderDate"])

    # New Feature
    df["TotalAmount"] = df["Quantity"] * df["Price"]

    logger.info(f"Duplicates removed: {duplicates_removed}")

    return df