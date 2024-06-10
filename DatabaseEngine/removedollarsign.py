import csv

def remove_dollar_sign(input_csv, output_csv):
    with open(input_csv, 'r') as file_in, open(output_csv, 'w', newline='') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)
        for row in reader:
            cleaned_row = [cell.replace('$', '') for cell in row]
            writer.writerow(cleaned_row)

# Usage example:
input_file = 'input.csv'
output_file = 'output.csv'
remove_dollar_sign(input_file, output_file)
