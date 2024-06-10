import pandas as pd

def xlsx_to_csv(xlsx_file, csv_file):
    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(xlsx_file)
    
    # Save DataFrame to CSV file
    df.to_csv(csv_file, index=False)

# Example usage:
xlsx_file = 'averagestatetuition.xlsx'
csv_file = 'averagestatetuition.csv'
xlsx_to_csv(xlsx_file, csv_file)
