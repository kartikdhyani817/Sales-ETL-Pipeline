REQUIRED_COLUMNS = [
    "OrderID",
    "CustomerName",
    "Product",
    "Category",
    "Quantity",
    "Price",
    "OrderDate",
    "City"
]

def validate_data(df):
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            raise Exception(f"Missing required column: {column}")

    if df.empty:
        raise Exception("Dataset is empty")

    return True