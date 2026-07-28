import os

import pandas as pd
import streamlit as st
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import zipfile
import tempfile

from config.database import engine


# ---------------------------------------------------------
# Streamlit page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Sales ETL Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# Custom dashboard styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            padding-top: 1rem;
        }

        .dashboard-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }

        .dashboard-subtitle {
            font-size: 1rem;
            color: #6b7280;
            margin-bottom: 1.5rem;
        }

        .status-success {
            padding: 0.7rem;
            border-radius: 0.5rem;
            background-color: rgba(34, 197, 94, 0.12);
            margin-bottom: 1rem;
        }

        .status-error {
            padding: 0.7rem;
            border-radius: 0.5rem;
            background-color: rgba(239, 68, 68, 0.12);
            margin-bottom: 1rem;
        }

        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            padding: 1rem;
            border-radius: 0.75rem;
        }

        div[data-testid="stSidebar"] {
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Database helper functions
# ---------------------------------------------------------

@st.cache_data(ttl=60)
def test_database_connection() -> tuple[bool, str]:
    """
    Test whether the Streamlit dashboard can connect to MySQL.

    Returns:
        tuple:
            - True and a success message when connected
            - False and the error message when connection fails
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return True, "MySQL database connected successfully."

    except SQLAlchemyError as error:
        return False, str(error)


@st.cache_data(ttl=60)
def load_sales_data() -> pd.DataFrame:
    """
    Load all records from the MySQL sales table.

    Returns:
        pandas.DataFrame: Sales data from MySQL.
    """

    query = text(
        """
        SELECT *
        FROM sales
        ORDER BY OrderDate;
        """
    )

    try:
        with engine.connect() as connection:
            dataframe = pd.read_sql(query, connection)

        if "OrderDate" in dataframe.columns:
            dataframe["OrderDate"] = pd.to_datetime(
                dataframe["OrderDate"],
                errors="coerce",
            )

        return dataframe

    except SQLAlchemyError as error:
        raise RuntimeError(
            f"Unable to load sales data from MySQL: {error}"
        ) from error


@st.cache_data(ttl=60)
def load_business_report() -> str:
    """
    Load the generated business report from the output directory.

    Returns:
        str: Contents of the business report.
    """

    report_path = "output/business_report.txt"

    if not os.path.exists(report_path):
        return (
            "Business report not found.\n\n"
            "Run `python main.py` first to generate the report."
        )

    with open(report_path, "r", encoding="utf-8") as report_file:
        return report_file.read()

@st.cache_data(ttl=60)
def calculate_dashboard_metrics(
    dataframe: pd.DataFrame,
) -> dict:
    """
    Calculate the main dashboard KPIs from the sales dataframe.

    Args:
        dataframe: Sales records loaded from MySQL.

    Returns:
        Dictionary containing dashboard KPI values.
    """

    if dataframe.empty:
        return {
            "total_revenue": 0.0,
            "total_orders": 0,
            "average_order_value": 0.0,
            "total_units": 0,
            "top_product": "No data",
        }

    required_columns = {
        "OrderID",
        "Product",
        "Quantity",
        "TotalAmount",
    }

    missing_columns = required_columns.difference(dataframe.columns)

    if missing_columns:
        raise ValueError(
            "The following required columns are missing: "
            + ", ".join(sorted(missing_columns))
        )

    total_revenue = dataframe["TotalAmount"].sum()

    total_orders = dataframe["OrderID"].nunique()

    average_order_value = (
        total_revenue / total_orders
        if total_orders > 0
        else 0.0
    )

    total_units = dataframe["Quantity"].sum()

    product_sales = (
        dataframe.groupby("Product", as_index=False)["Quantity"]
        .sum()
        .sort_values("Quantity", ascending=False)
    )

    top_product = (
        product_sales.iloc[0]["Product"]
        if not product_sales.empty
        else "No data"
    )

    return {
        "total_revenue": float(total_revenue),
        "total_orders": int(total_orders),
        "average_order_value": float(average_order_value),
        "total_units": int(total_units),
        "top_product": str(top_product),
    }

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown(
    '<div class="dashboard-title">📊 Sales ETL Dashboard</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="dashboard-subtitle">
        Interactive analytics dashboard powered by Python, MySQL,
        SQLAlchemy and Streamlit.
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------

with st.sidebar:

    st.title("Sales ETL")

    st.caption(
        "End-to-end data pipeline and business analytics dashboard"
    )

    st.divider()

    selected_page = st.radio(
        "Navigation",
        options=[
            "Dashboard",
            "Analytics",
            "Sales Data",
            "Business Report",
            "Downloads",
        ],
        index=0,
    )

    st.divider()

    st.subheader("Pipeline")

    if st.button(
        "Refresh dashboard",
        use_container_width=True,
    ):
        st.cache_data.clear()
        st.rerun()

    st.caption(
        "Run `python main.py` whenever the raw dataset changes."
    )

    st.divider()

    st.caption("Created by Kartik Dhyani")


# ---------------------------------------------------------
# Database connection status
# ---------------------------------------------------------

connection_status, connection_message = test_database_connection()

if connection_status:

    st.markdown(
        f"""
        <div class="status-success">
            ✅ {connection_message}
        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    st.markdown(
        """
        <div class="status-error">
            ❌ Unable to connect to the MySQL database.
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("View database error"):
        st.code(connection_message)

    st.warning(
        "Check your MySQL service, database name and `.env` credentials."
    )

    st.stop()


# ---------------------------------------------------------
# Load dashboard data
# ---------------------------------------------------------

try:
    sales_df = load_sales_data()

except RuntimeError as error:

    st.error(str(error))

    st.info(
        "Run `python main.py` first so the ETL pipeline creates "
        "and loads the `sales` table."
    )

    st.stop()


# ---------------------------------------------------------
# Initial page placeholders
# ---------------------------------------------------------

if selected_page == "Dashboard":

    st.subheader("Dashboard Overview")

    if sales_df.empty:

        st.warning(
            "The sales table does not contain any records."
        )

        st.stop()

    try:
        metrics = calculate_dashboard_metrics(sales_df)

    except ValueError as error:
        st.error(str(error))
        st.stop()

    # -----------------------------------------------------
    # KPI cards
    # -----------------------------------------------------

    kpi_column_1, kpi_column_2, kpi_column_3, kpi_column_4 = (
        st.columns(4)
    )

    with kpi_column_1:
        st.metric(
            label="Total Revenue",
            value=f"₹{metrics['total_revenue']:,.2f}",
        )

    with kpi_column_2:
        st.metric(
            label="Total Orders",
            value=f"{metrics['total_orders']:,}",
        )

    with kpi_column_3:
        st.metric(
            label="Average Order Value",
            value=f"₹{metrics['average_order_value']:,.2f}",
        )

    with kpi_column_4:
        st.metric(
            label="Units Sold",
            value=f"{metrics['total_units']:,}",
        )

    st.markdown("")

    st.success(
        f"🏆 Top-selling product: **{metrics['top_product']}**"
    )

    st.divider()

    # -----------------------------------------------------
    # Prepare dashboard charts
    # -----------------------------------------------------

    chart_column_1, chart_column_2 = st.columns(2)

    with chart_column_1:

        st.subheader("Revenue by Category")

        if "Category" in sales_df.columns:

            category_revenue = (
                sales_df.groupby(
                    "Category",
                    as_index=False,
                )["TotalAmount"]
                .sum()
                .sort_values(
                    "TotalAmount",
                    ascending=False,
                )
            )

            category_chart_data = (
                category_revenue.set_index("Category")
            )

            st.bar_chart(
                category_chart_data,
                y="TotalAmount",
                use_container_width=True,
            )

        else:
            st.warning(
                "Category column is unavailable."
            )

    with chart_column_2:

        st.subheader("Monthly Revenue Trend")

        if (
            "OrderDate" in sales_df.columns
            and sales_df["OrderDate"].notna().any()
        ):

            monthly_dataframe = sales_df.copy()

            monthly_dataframe["Month"] = (
                monthly_dataframe["OrderDate"]
                .dt.to_period("M")
                .astype(str)
            )

            monthly_revenue = (
                monthly_dataframe.groupby(
                    "Month",
                    as_index=False,
                )["TotalAmount"]
                .sum()
                .sort_values("Month")
            )

            monthly_chart_data = (
                monthly_revenue.set_index("Month")
            )

            st.line_chart(
                monthly_chart_data,
                y="TotalAmount",
                use_container_width=True,
            )

        else:
            st.warning(
                "Valid order dates are unavailable."
            )

    st.divider()

    # -----------------------------------------------------
    # Top products
    # -----------------------------------------------------

    st.subheader("Top Products by Units Sold")

    if {
        "Product",
        "Quantity",
    }.issubset(sales_df.columns):

        top_products = (
            sales_df.groupby(
                "Product",
                as_index=False,
            )["Quantity"]
            .sum()
            .sort_values(
                "Quantity",
                ascending=False,
            )
            .head(5)
        )

        top_products_chart = (
            top_products.set_index("Product")
        )

        st.bar_chart(
            top_products_chart,
            y="Quantity",
            use_container_width=True,
        )

    else:
        st.warning(
            "Product or Quantity column is unavailable."
        )

    st.divider()

    # -----------------------------------------------------
    # Recent transactions
    # -----------------------------------------------------

    st.subheader("Recent Sales Transactions")

    recent_sales = sales_df.copy()

    if "OrderDate" in recent_sales.columns:

        recent_sales = recent_sales.sort_values(
            "OrderDate",
            ascending=False,
        )

    preferred_columns = [
        "OrderID",
        "CustomerName",
        "Product",
        "Category",
        "Quantity",
        "Price",
        "TotalAmount",
        "OrderDate",
        "City",
    ]

    available_columns = [
        column
        for column in preferred_columns
        if column in recent_sales.columns
    ]

    if available_columns:
        recent_sales = recent_sales[available_columns]

    st.dataframe(
        recent_sales.head(10),
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        "Showing the 10 most recent sales transactions."
    )

elif selected_page == "Analytics":

    st.subheader("Sales Analytics")

    if sales_df.empty:
        st.warning("The sales table does not contain any records.")
        st.stop()

    analytics_df = sales_df.copy()

    st.markdown(
        "Use the filters below to explore sales performance."
    )

    # -----------------------------------------------------
    # Filter options
    # -----------------------------------------------------

    filter_column_1, filter_column_2, filter_column_3 = (
        st.columns(3)
    )

    with filter_column_1:

        if "Category" in analytics_df.columns:

            category_options = sorted(
                analytics_df["Category"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_categories = st.multiselect(
                "Select categories",
                options=category_options,
                default=category_options,
            )

        else:
            selected_categories = []

    with filter_column_2:

        if "City" in analytics_df.columns:

            city_options = sorted(
                analytics_df["City"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_cities = st.multiselect(
                "Select cities",
                options=city_options,
                default=city_options,
            )

        else:
            selected_cities = []

    with filter_column_3:

        if "Product" in analytics_df.columns:

            product_options = sorted(
                analytics_df["Product"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_products = st.multiselect(
                "Select products",
                options=product_options,
                default=product_options,
            )

        else:
            selected_products = []

    # -----------------------------------------------------
    # Date filter
    # -----------------------------------------------------

    if (
        "OrderDate" in analytics_df.columns
        and analytics_df["OrderDate"].notna().any()
    ):

        minimum_date = analytics_df["OrderDate"].min().date()
        maximum_date = analytics_df["OrderDate"].max().date()

        selected_date_range = st.date_input(
            "Select order date range",
            value=(minimum_date, maximum_date),
            min_value=minimum_date,
            max_value=maximum_date,
        )

    else:
        selected_date_range = None

    # -----------------------------------------------------
    # Apply filters
    # -----------------------------------------------------

    if selected_categories and "Category" in analytics_df.columns:

        analytics_df = analytics_df[
            analytics_df["Category"]
            .astype(str)
            .isin(selected_categories)
        ]

    if selected_cities and "City" in analytics_df.columns:

        analytics_df = analytics_df[
            analytics_df["City"]
            .astype(str)
            .isin(selected_cities)
        ]

    if selected_products and "Product" in analytics_df.columns:

        analytics_df = analytics_df[
            analytics_df["Product"]
            .astype(str)
            .isin(selected_products)
        ]

    if (
        selected_date_range
        and len(selected_date_range) == 2
        and "OrderDate" in analytics_df.columns
    ):

        start_date = pd.to_datetime(selected_date_range[0])
        end_date = pd.to_datetime(selected_date_range[1])

        analytics_df = analytics_df[
            analytics_df["OrderDate"].between(
                start_date,
                end_date,
            )
        ]

    # -----------------------------------------------------
    # Reset filters button
    # -----------------------------------------------------

    if st.button("Reset analytics filters"):

        st.cache_data.clear()
        st.rerun()

    st.divider()

    # -----------------------------------------------------
    # Filtered KPI summary
    # -----------------------------------------------------

    if analytics_df.empty:

        st.warning(
            "No sales records match the selected filters."
        )

        st.stop()

    filtered_revenue = (
        analytics_df["TotalAmount"].sum()
        if "TotalAmount" in analytics_df.columns
        else 0
    )

    filtered_orders = (
        analytics_df["OrderID"].nunique()
        if "OrderID" in analytics_df.columns
        else len(analytics_df)
    )

    filtered_units = (
        analytics_df["Quantity"].sum()
        if "Quantity" in analytics_df.columns
        else 0
    )

    filtered_average_order = (
        filtered_revenue / filtered_orders
        if filtered_orders > 0
        else 0
    )

    summary_column_1, summary_column_2, summary_column_3, summary_column_4 = (
        st.columns(4)
    )

    with summary_column_1:

        st.metric(
            "Filtered Revenue",
            f"₹{filtered_revenue:,.2f}",
        )

    with summary_column_2:

        st.metric(
            "Filtered Orders",
            f"{filtered_orders:,}",
        )

    with summary_column_3:

        st.metric(
            "Filtered Units",
            f"{int(filtered_units):,}",
        )

    with summary_column_4:

        st.metric(
            "Average Order Value",
            f"₹{filtered_average_order:,.2f}",
        )

    st.divider()

    # -----------------------------------------------------
    # Revenue charts
    # -----------------------------------------------------

    revenue_column_1, revenue_column_2 = st.columns(2)

    with revenue_column_1:

        st.subheader("Revenue by Category")

        if {
            "Category",
            "TotalAmount",
        }.issubset(analytics_df.columns):

            category_revenue = (
                analytics_df.groupby(
                    "Category",
                    as_index=False,
                )["TotalAmount"]
                .sum()
                .sort_values(
                    "TotalAmount",
                    ascending=False,
                )
            )

            st.bar_chart(
                category_revenue.set_index("Category"),
                y="TotalAmount",
                use_container_width=True,
            )

        else:
            st.warning(
                "Category or TotalAmount column is unavailable."
            )

    with revenue_column_2:

        st.subheader("Revenue by City")

        if {
            "City",
            "TotalAmount",
        }.issubset(analytics_df.columns):

            city_revenue = (
                analytics_df.groupby(
                    "City",
                    as_index=False,
                )["TotalAmount"]
                .sum()
                .sort_values(
                    "TotalAmount",
                    ascending=False,
                )
            )

            st.bar_chart(
                city_revenue.set_index("City"),
                y="TotalAmount",
                use_container_width=True,
            )

        else:
            st.warning(
                "City or TotalAmount column is unavailable."
            )

    st.divider()

    # -----------------------------------------------------
    # Product analytics
    # -----------------------------------------------------

    product_column_1, product_column_2 = st.columns(2)

    with product_column_1:

        st.subheader("Units Sold by Product")

        if {
            "Product",
            "Quantity",
        }.issubset(analytics_df.columns):

            product_units = (
                analytics_df.groupby(
                    "Product",
                    as_index=False,
                )["Quantity"]
                .sum()
                .sort_values(
                    "Quantity",
                    ascending=False,
                )
                .head(10)
            )

            st.bar_chart(
                product_units.set_index("Product"),
                y="Quantity",
                use_container_width=True,
            )

        else:
            st.warning(
                "Product or Quantity column is unavailable."
            )

    with product_column_2:

        st.subheader("Revenue by Product")

        if {
            "Product",
            "TotalAmount",
        }.issubset(analytics_df.columns):

            product_revenue = (
                analytics_df.groupby(
                    "Product",
                    as_index=False,
                )["TotalAmount"]
                .sum()
                .sort_values(
                    "TotalAmount",
                    ascending=False,
                )
                .head(10)
            )

            st.bar_chart(
                product_revenue.set_index("Product"),
                y="TotalAmount",
                use_container_width=True,
            )

        else:
            st.warning(
                "Product or TotalAmount column is unavailable."
            )

    st.divider()

    # -----------------------------------------------------
    # Monthly revenue trend
    # -----------------------------------------------------

    st.subheader("Monthly Revenue Trend")

    if (
        "OrderDate" in analytics_df.columns
        and "TotalAmount" in analytics_df.columns
        and analytics_df["OrderDate"].notna().any()
    ):

        monthly_sales_df = analytics_df.copy()

        monthly_sales_df["Month"] = (
            monthly_sales_df["OrderDate"]
            .dt.to_period("M")
            .astype(str)
        )

        monthly_revenue = (
            monthly_sales_df.groupby(
                "Month",
                as_index=False,
            )["TotalAmount"]
            .sum()
            .sort_values("Month")
        )

        st.line_chart(
            monthly_revenue.set_index("Month"),
            y="TotalAmount",
            use_container_width=True,
        )

    else:
        st.warning(
            "Valid order dates or revenue data are unavailable."
        )

    st.divider()

    # -----------------------------------------------------
    # Filtered records
    # -----------------------------------------------------

    st.subheader("Filtered Sales Records")

    preferred_columns = [
        "OrderID",
        "CustomerName",
        "Product",
        "Category",
        "Quantity",
        "Price",
        "TotalAmount",
        "OrderDate",
        "City",
    ]

    available_columns = [
        column
        for column in preferred_columns
        if column in analytics_df.columns
    ]

    filtered_display_df = (
        analytics_df[available_columns]
        if available_columns
        else analytics_df
    )

    st.dataframe(
        filtered_display_df,
        use_container_width=True,
        hide_index=True,
    )

    st.caption(
        f"Showing {len(filtered_display_df):,} filtered records."
    )

elif selected_page == "Sales Data":

    st.subheader("Sales Database")

    if sales_df.empty:
        st.warning("The sales table does not contain any records.")
        st.stop()

    database_df = sales_df.copy()

    st.markdown(
        "Search, filter and inspect records loaded from the MySQL database."
    )

    # -----------------------------------------------------
    # Search box
    # -----------------------------------------------------

    search_text = st.text_input(
        "Search records",
        placeholder="Search by order ID, customer, product, category or city",
    )

    if search_text:

        search_text = search_text.strip().lower()

        searchable_columns = [
            column
            for column in [
                "OrderID",
                "CustomerName",
                "Customer Name",
                "Product",
                "Category",
                "City",
            ]
            if column in database_df.columns
        ]

        if searchable_columns:

            search_mask = pd.Series(
                False,
                index=database_df.index,
            )

            for column in searchable_columns:

                search_mask = search_mask | (
                    database_df[column]
                    .astype(str)
                    .str.lower()
                    .str.contains(
                        search_text,
                        na=False,
                        regex=False,
                    )
                )

            database_df = database_df[search_mask]

    # -----------------------------------------------------
    # Filter controls
    # -----------------------------------------------------

    filter_column_1, filter_column_2, filter_column_3 = st.columns(3)

    with filter_column_1:

        if "Category" in database_df.columns:

            category_options = sorted(
                sales_df["Category"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_database_categories = st.multiselect(
                "Filter by category",
                options=category_options,
                default=[],
                key="database_category_filter",
            )

        else:
            selected_database_categories = []

    with filter_column_2:

        if "City" in database_df.columns:

            city_options = sorted(
                sales_df["City"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_database_cities = st.multiselect(
                "Filter by city",
                options=city_options,
                default=[],
                key="database_city_filter",
            )

        else:
            selected_database_cities = []

    with filter_column_3:

        if "Product" in database_df.columns:

            product_options = sorted(
                sales_df["Product"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_database_products = st.multiselect(
                "Filter by product",
                options=product_options,
                default=[],
                key="database_product_filter",
            )

        else:
            selected_database_products = []

    # -----------------------------------------------------
    # Apply filters
    # -----------------------------------------------------

    if (
        selected_database_categories
        and "Category" in database_df.columns
    ):

        database_df = database_df[
            database_df["Category"]
            .astype(str)
            .isin(selected_database_categories)
        ]

    if (
        selected_database_cities
        and "City" in database_df.columns
    ):

        database_df = database_df[
            database_df["City"]
            .astype(str)
            .isin(selected_database_cities)
        ]

    if (
        selected_database_products
        and "Product" in database_df.columns
    ):

        database_df = database_df[
            database_df["Product"]
            .astype(str)
            .isin(selected_database_products)
        ]

    # -----------------------------------------------------
    # Numeric filters
    # -----------------------------------------------------

    numeric_filter_column_1, numeric_filter_column_2 = st.columns(2)

    with numeric_filter_column_1:

        if (
            "TotalAmount" in sales_df.columns
            and sales_df["TotalAmount"].notna().any()
        ):

            minimum_revenue = float(
                sales_df["TotalAmount"].min()
            )

            maximum_revenue = float(
                sales_df["TotalAmount"].max()
            )

            selected_revenue_range = st.slider(
                "Total amount range",
                min_value=minimum_revenue,
                max_value=maximum_revenue,
                value=(
                    minimum_revenue,
                    maximum_revenue,
                ),
            )

            database_df = database_df[
                database_df["TotalAmount"].between(
                    selected_revenue_range[0],
                    selected_revenue_range[1],
                )
            ]

    with numeric_filter_column_2:

        if (
            "Quantity" in sales_df.columns
            and sales_df["Quantity"].notna().any()
        ):

            minimum_quantity = int(
                sales_df["Quantity"].min()
            )

            maximum_quantity = int(
                sales_df["Quantity"].max()
            )

            selected_quantity_range = st.slider(
                "Quantity range",
                min_value=minimum_quantity,
                max_value=maximum_quantity,
                value=(
                    minimum_quantity,
                    maximum_quantity,
                ),
            )

            database_df = database_df[
                database_df["Quantity"].between(
                    selected_quantity_range[0],
                    selected_quantity_range[1],
                )
            ]

    # -----------------------------------------------------
    # Date filter
    # -----------------------------------------------------

    if (
        "OrderDate" in sales_df.columns
        and sales_df["OrderDate"].notna().any()
    ):

        minimum_database_date = (
            sales_df["OrderDate"].min().date()
        )

        maximum_database_date = (
            sales_df["OrderDate"].max().date()
        )

        selected_database_dates = st.date_input(
            "Filter by order date",
            value=(
                minimum_database_date,
                maximum_database_date,
            ),
            min_value=minimum_database_date,
            max_value=maximum_database_date,
            key="database_date_filter",
        )

        if len(selected_database_dates) == 2:

            database_start_date = pd.to_datetime(
                selected_database_dates[0]
            )

            database_end_date = pd.to_datetime(
                selected_database_dates[1]
            )

            database_df = database_df[
                database_df["OrderDate"].between(
                    database_start_date,
                    database_end_date,
                )
            ]

    # -----------------------------------------------------
    # Sort controls
    # -----------------------------------------------------

    sort_column_1, sort_column_2 = st.columns(2)

    with sort_column_1:

        sortable_columns = [
            column
            for column in [
                "OrderID",
                "CustomerName",
                "Customer Name",
                "Product",
                "Category",
                "Quantity",
                "Price",
                "TotalAmount",
                "OrderDate",
                "City",
            ]
            if column in database_df.columns
        ]

        selected_sort_column = st.selectbox(
            "Sort by",
            options=sortable_columns,
            index=(
                sortable_columns.index("OrderDate")
                if "OrderDate" in sortable_columns
                else 0
            ),
        )

    with sort_column_2:

        selected_sort_order = st.selectbox(
            "Sort order",
            options=[
                "Descending",
                "Ascending",
            ],
        )

    if selected_sort_column:

        database_df = database_df.sort_values(
            selected_sort_column,
            ascending=(
                selected_sort_order == "Ascending"
            ),
            na_position="last",
        )

    # -----------------------------------------------------
    # Database statistics
    # -----------------------------------------------------

    st.divider()

    result_rows = len(database_df)

    total_database_revenue = (
        database_df["TotalAmount"].sum()
        if "TotalAmount" in database_df.columns
        else 0
    )

    total_database_units = (
        database_df["Quantity"].sum()
        if "Quantity" in database_df.columns
        else 0
    )

    average_database_value = (
        database_df["TotalAmount"].mean()
        if (
            "TotalAmount" in database_df.columns
            and not database_df.empty
        )
        else 0
    )

    statistics_column_1, statistics_column_2, statistics_column_3, statistics_column_4 = (
        st.columns(4)
    )

    with statistics_column_1:

        st.metric(
            "Matching Records",
            f"{result_rows:,}",
        )

    with statistics_column_2:

        st.metric(
            "Filtered Revenue",
            f"₹{total_database_revenue:,.2f}",
        )

    with statistics_column_3:

        st.metric(
            "Filtered Units",
            f"{int(total_database_units):,}",
        )

    with statistics_column_4:

        st.metric(
            "Average Sale Value",
            f"₹{average_database_value:,.2f}",
        )

    st.divider()

    # -----------------------------------------------------
    # Select displayed columns
    # -----------------------------------------------------

    st.subheader("Sales Records")

    default_columns = [
        column
        for column in [
            "OrderID",
            "CustomerName",
            "Customer Name",
            "Product",
            "Category",
            "Quantity",
            "Price",
            "TotalAmount",
            "OrderDate",
            "City",
        ]
        if column in database_df.columns
    ]

    selected_display_columns = st.multiselect(
        "Choose columns to display",
        options=database_df.columns.tolist(),
        default=default_columns,
    )

    if selected_display_columns:

        display_database_df = database_df[
            selected_display_columns
        ].copy()

    else:

        display_database_df = database_df.copy()

    # -----------------------------------------------------
    # Format display columns
    # -----------------------------------------------------

    column_configuration = {}

    if "Price" in display_database_df.columns:

        column_configuration["Price"] = st.column_config.NumberColumn(
            "Price",
            format="₹%.2f",
        )

    if "TotalAmount" in display_database_df.columns:

        column_configuration["TotalAmount"] = (
            st.column_config.NumberColumn(
                "Total Amount",
                format="₹%.2f",
            )
        )

    if "Quantity" in display_database_df.columns:

        column_configuration["Quantity"] = (
            st.column_config.NumberColumn(
                "Quantity",
                format="%d",
            )
        )

    if "OrderDate" in display_database_df.columns:

        column_configuration["OrderDate"] = (
            st.column_config.DatetimeColumn(
                "Order Date",
                format="DD-MM-YYYY",
            )
        )

    st.dataframe(
        display_database_df,
        use_container_width=True,
        hide_index=True,
        column_config=column_configuration,
    )

    st.caption(
        f"Showing {len(display_database_df):,} of "
        f"{len(sales_df):,} total records."
    )

    # -----------------------------------------------------
    # CSV preview download
    # -----------------------------------------------------

    csv_data = display_database_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download filtered records as CSV",
        data=csv_data,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

elif selected_page == "Business Report":

    st.subheader("Business Report")

    st.markdown(
        "Review the business report generated automatically by the ETL pipeline."
    )

    report_text = load_business_report()

    report_path = "output/business_report.txt"

    # -----------------------------------------------------
    # Report status
    # -----------------------------------------------------

    if not os.path.exists(report_path):

        st.warning(
            "The business report has not been generated yet."
        )

        st.info(
            "Run `python main.py` first to generate the report."
        )

        st.stop()

    st.success(
        "Business report loaded successfully."
    )

    st.divider()

    # -----------------------------------------------------
    # Report summary
    # -----------------------------------------------------

    report_column_1, report_column_2, report_column_3 = (
        st.columns(3)
    )

    with report_column_1:

        st.metric(
            "Report Status",
            "Available",
        )

    with report_column_2:

        report_size = os.path.getsize(report_path)

        st.metric(
            "File Size",
            f"{report_size:,} bytes",
        )

    with report_column_3:

        report_lines = len(report_text.splitlines())

        st.metric(
            "Report Lines",
            f"{report_lines:,}",
        )

    st.divider()

    # -----------------------------------------------------
    # Report viewer
    # -----------------------------------------------------

    st.subheader("Generated Report")

    st.text_area(
        label="Business report content",
        value=report_text,
        height=500,
        disabled=True,
        label_visibility="collapsed",
    )

    st.divider()

    # -----------------------------------------------------
    # Report download
    # -----------------------------------------------------

    st.download_button(
        label="Download Business Report",
        data=report_text,
        file_name="business_report.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.divider()

    # -----------------------------------------------------
    # SQL query reference
    # -----------------------------------------------------

    st.subheader("SQL Analytics Used")

    st.markdown(
        "The report is generated from SQL queries executed against the MySQL `sales` table."
    )

    with st.expander("Total Revenue Query"):

        st.code(
            """
SELECT
    SUM(TotalAmount) AS TotalRevenue
FROM sales;
            """,
            language="sql",
        )

    with st.expander("Total Orders Query"):

        st.code(
            """
SELECT
    COUNT(DISTINCT OrderID) AS TotalOrders
FROM sales;
            """,
            language="sql",
        )

    with st.expander("Average Order Value Query"):

        st.code(
            """
SELECT
    ROUND(AVG(TotalAmount), 2) AS AverageOrderValue
FROM sales;
            """,
            language="sql",
        )

    with st.expander("Top-Selling Product Query"):

        st.code(
            """
SELECT
    Product,
    SUM(Quantity) AS TotalUnitsSold
FROM sales
GROUP BY Product
ORDER BY TotalUnitsSold DESC
LIMIT 1;
            """,
            language="sql",
        )

    with st.expander("Revenue by Category Query"):

        st.code(
            """
SELECT
    Category,
    SUM(TotalAmount) AS Revenue
FROM sales
GROUP BY Category
ORDER BY Revenue DESC;
            """,
            language="sql",
        )

    with st.expander("Revenue by City Query"):

        st.code(
            """
SELECT
    City,
    SUM(TotalAmount) AS Revenue
FROM sales
GROUP BY City
ORDER BY Revenue DESC;
            """,
            language="sql",
        )

    with st.expander("Monthly Revenue Query"):

        st.code(
            """
SELECT
    DATE_FORMAT(OrderDate, '%Y-%m') AS Month,
    SUM(TotalAmount) AS Revenue
FROM sales
GROUP BY Month
ORDER BY Month;
            """,
            language="sql",
        )

    st.divider()

    # -----------------------------------------------------
    # Report generation information
    # -----------------------------------------------------

    st.subheader("Report Generation Process")

    st.markdown(
        """
The report is produced automatically through the following steps:

1. The raw CSV file is loaded.
2. Missing values and duplicate records are handled.
3. New calculated fields such as `TotalAmount` are created.
4. Cleaned data is saved as a Parquet file.
5. The processed data is loaded into MySQL.
6. SQL analytics queries calculate business KPIs.
7. The results are written to `output/business_report.txt`.
        """
    )

    st.info(
        "Run `python main.py` whenever the raw dataset changes to refresh the report."
    )

elif selected_page == "Downloads":

    st.subheader("Download Centre")

    st.markdown(
        "Download generated outputs from the ETL pipeline."
    )

    st.divider()

    # -------------------------------------------------------
    # Business Report
    # -------------------------------------------------------

    report_file = "output/business_report.txt"

    if os.path.exists(report_file):

        with open(report_file, "rb") as f:

            st.download_button(
                "Download Business Report",
                f.read(),
                file_name="business_report.txt",
                mime="text/plain",
                use_container_width=True,
            )

    # -------------------------------------------------------
    # Processed CSV
    # -------------------------------------------------------

    if not sales_df.empty:

        csv = sales_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Sales CSV",
            csv,
            file_name="sales.csv",
            mime="text/csv",
            use_container_width=True,
        )

    # -------------------------------------------------------
    # Parquet File
    # -------------------------------------------------------

    parquet_file = "data/processed/clean_sales.parquet"

    if os.path.exists(parquet_file):

        with open(parquet_file, "rb") as f:

            st.download_button(
                "Download Parquet",
                f.read(),
                file_name="clean_sales.parquet",
                mime="application/octet-stream",
                use_container_width=True,
            )

    st.divider()

    # -------------------------------------------------------
    # Charts ZIP
    # -------------------------------------------------------

    chart_folder = "output/charts"

    if os.path.exists(chart_folder):

        temp_zip = tempfile.NamedTemporaryFile(delete=False, suffix=".zip")

        with zipfile.ZipFile(
            temp_zip.name,
            "w",
            zipfile.ZIP_DEFLATED,
        ) as zipf:

            for file in os.listdir(chart_folder):

                path = os.path.join(chart_folder, file)

                if os.path.isfile(path):

                    zipf.write(
                        path,
                        arcname=file,
                    )

        with open(temp_zip.name, "rb") as f:

            st.download_button(
                "Download Charts ZIP",
                f.read(),
                file_name="charts.zip",
                mime="application/zip",
                use_container_width=True,
            )

    st.divider()

    # -------------------------------------------------------
    # Project Information
    # -------------------------------------------------------

    st.subheader("Project Information")

    st.markdown(
        """
### Sales ETL Pipeline

A complete Data Engineering project demonstrating an end-to-end ETL workflow.

### Features

- CSV Ingestion
- Data Validation
- Data Cleaning
- Feature Engineering
- Parquet Export
- MySQL Loading
- SQL Analytics
- Business Report Generation
- Data Visualization
- Interactive Dashboard

### Technologies

- Python
- Pandas
- MySQL
- SQLAlchemy
- Streamlit
- Matplotlib
- PyArrow

### ETL Workflow

CSV

↓

Validation

↓

Cleaning

↓

Feature Engineering

↓

Parquet

↓

MySQL

↓

SQL Analytics

↓

Business Report

↓

Dashboard
"""
    )

    st.divider()

    st.success(
        "Sales ETL Pipeline completed successfully."
    )

    st.caption(
        "Developed by Kartik Dhyani"
    )