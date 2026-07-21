import pandas as pd

from utils.logger import logger
from scripts.validate import validate_data

def load_data(file_path):
    logger.info("Reading CSV file")

    df = pd.read_csv(file_path)

    validate_data(df)

    logger.info(f"{len(df)} records loaded successfully")

    return df
