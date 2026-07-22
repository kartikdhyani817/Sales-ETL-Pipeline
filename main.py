from scripts.ingest import load_data
from scripts.clean import clean_data
from scripts.save import save_data
from scripts.report import generate_report

from utils.logger import logger


def main():

    print("Pipeline Started...\n")

    df = load_data("data/raw/sales_data.csv")

    df = clean_data(df)

    generate_report(df)

    save_data(df)

    print(df)

    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
