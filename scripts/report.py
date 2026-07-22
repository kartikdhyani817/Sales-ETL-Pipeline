def generate_report(df):

    print("\n========== DATA QUALITY REPORT ==========\n")

    print(f"Rows : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    print("\nMissing Values\n")

    print(df.isnull().sum())

    print("\nDuplicate Rows :", df.duplicated().sum())

    print("\n=========================================\n")