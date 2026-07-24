from scripts.ingest import load_data
from scripts.clean import clean_data
from scripts.report import generate_report
from scripts.save import save_data
from scripts.load_mysql import test_connection, load_to_mysql
from utils.logger import logger


def main():

    print("Pipeline Started...\n")

    test_connection()

    df = load_data("data/raw/sales_data.csv")

    df = clean_data(df)

    generate_report(df)

    save_data(df)

    load_to_mysql(df)

    print("\nPipeline Completed Successfully.")

    logger.info("Pipeline Completed")


if __name__ == "__main__":
    main()
