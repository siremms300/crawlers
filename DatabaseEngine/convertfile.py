import pandas as pd

def csv_to_xlsx(csv_file, xlsx_file):
    # Read CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file)

    # Save DataFrame to Excel file
    df.to_excel(xlsx_file, index=False)

# Example usage:
csv_file = 'universitiestest.csv'
xlsx_file = 'universitiesdata.xlsx'
csv_to_xlsx(csv_file, xlsx_file)
