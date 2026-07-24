from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from config.database import engine
from utils.logger import logger


def test_connection():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("MySQL Connected Successfully.")
        logger.info("Database connected")

    except SQLAlchemyError as e:
        logger.error(e)
        raise


def load_to_mysql(df):

    try:

        df.to_sql(
            name="sales",
            con=engine,
            if_exists="replace",
            index=False
        )

        print("Data loaded into MySQL successfully.")
        logger.info("Data loaded into MySQL")

    except Exception as e:
        logger.error(e)
        raise