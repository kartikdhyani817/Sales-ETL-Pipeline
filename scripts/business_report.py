import os


def generate_business_report(results):

    os.makedirs("output", exist_ok=True)

    report_path = "output/business_report.txt"

    with open(report_path, "w") as file:

        file.write("SALES BUSINESS REPORT\n")
        file.write("=" * 40 + "\n\n")

        for title, dataframe in results.items():

            file.write(title + "\n")
            file.write("-" * 30 + "\n")

            file.write(dataframe.to_string(index=False))

            file.write("\n\n")

    print(f"\nBusiness report generated:\n{report_path}")