

def main():

    print("Pipeline Started...\n")

    test_connection()

    df = load_data("data/raw/sales_data.csv")

    df = clean_data(df)

    generate_report(df)

    save_data(df)

    load_to_mysql(df)

    results = run_analytics()

    generate_business_report(results)

    generate_charts()

    print("\nPipeline Completed Successfully.")

    logger.info("Pipeline Completed")


if __name__ == "__main__":
    main()
