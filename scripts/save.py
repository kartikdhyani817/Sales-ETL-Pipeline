import os
from utils.logger import logger


def save_data(df):

    os.makedirs("data/processed", exist_ok=True)

    output_path = "data/processed/clean_sales.parquet"

    df.to_parquet(output_path, index=False)

    logger.info("Processed data saved successfully")

    print(f"\nClean data saved to:\n{output_path}")