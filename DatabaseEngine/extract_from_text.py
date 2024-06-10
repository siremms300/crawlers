import csv
import re
import os

# The input text you provided
input_text = """



Name (international):

University of Alaska Southeast, Sitka Campus

Name (local):

University of Alaska Southeast

Type of institution:

University

Address:

1332 Seward Avenue

City:

Sitka, Alaska

Phone:

+1 (907) 747-7700,+1 (800) 478-6653

Fax:

Email:

student.info[at]uas.alaska.edu




"""

# Function to extract the information using regular expressions
def extract_information(text):
    info = {}
    info['Name (international)'] = re.search(r"Name \(international\):\s*(.*)\s*Name \(local\):", text, re.DOTALL).group(1).strip()
    info['Name (local)'] = re.search(r"Name \(local\):\s*(.*)\s*Type of institution:", text, re.DOTALL).group(1).strip()
    info['Type of institution'] = re.search(r"Type of institution:\s*(.*)\s*Address:", text, re.DOTALL).group(1).strip()
    info['Address'] = re.search(r"Address:\s*(.*)\s*City:", text, re.DOTALL).group(1).strip()
    info['City'] = re.search(r"City:\s*(.*)\s*Phone:", text, re.DOTALL).group(1).strip()
    info['Phone'] = re.search(r"Phone:\s*(.*)\s*Fax:", text, re.DOTALL).group(1).strip()
    info['Fax'] = re.search(r"Fax:\s*(.*)\s*Email:", text, re.DOTALL).group(1).strip()
    info['Email'] = re.search(r"Email:\s*(.*)", text, re.DOTALL).group(1).strip().replace('[at]', '@')
    return info

# Function to check if the data already exists in the CSV file
def data_exists(file, data):
    if not os.path.isfile(file):
        return False
    with open(file, mode='r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row == data:
                return True
    return False

# Extract information
information = extract_information(input_text)

# Define the CSV file name
csv_file = 'university_info.csv'

# Check if the data already exists
if not data_exists(csv_file, information):
    # Write the information to the CSV file
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=information.keys())
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(information)
    print(f"Information saved to {csv_file}")
else:
    print(f"Information already exists in {csv_file}")
