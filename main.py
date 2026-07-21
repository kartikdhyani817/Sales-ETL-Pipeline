from scripts.ingest import load_data
from utils.logger import logger


def main():
    print("Pipeline started...")

    file_path = "data/raw/sales_data.csv"
    df = load_data(file_path)

    print("\nSales data loaded successfully:\n")
    print(df.to_string(index=False))

    logger.info("Pipeline executed successfully")


if __name__ == "__main__":
    main()