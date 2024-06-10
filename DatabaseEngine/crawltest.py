import os.path
import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor
import random
import time

# List of user-agents to rotate
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
]

# Function to crawl the webpage and extract university data
def crawl_and_extract(url):
    # Choose a random user-agent from the list
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <div> tags with class "univer_cont_detail"
        university_details = soup.find_all('div', class_='univer_cont_detail')
        
        university_data = {}
        
        for detail in university_details:
            # Check if cont_title and p tag exist before accessing get_text()
            title_element = detail.find('div', class_='cont_title').find('p')
            title = title_element.get_text(strip=True) if title_element else "N/A"
            
            # Check if cont_info and p tag exist before accessing get_text()
            info_element = detail.find('div', class_='cont_info').p
            info = info_element.get_text(strip=True) if info_element else "N/A"
                
            university_data[title] = info
        
        return university_data
    else:
        print(f"Failed to fetch page {url}: {response.status_code}")
        return None

# Function to write data to CSV file
def write_to_csv(data, filename):
    # Check if the CSV file already exists
    file_exists = os.path.isfile(filename)
    
    # If file exists and is not empty, don't write the header row
    if file_exists and os.path.getsize(filename) > 0:
        mode = "a"  # Append mode
    else:
        mode = "w"  # Write mode
    
    # Transpose the data for writing to CSV
    keys = data[0].keys()
    transposed_data = [[result.get(key, "N/A") for key in keys] for result in data]
    
    # Write the transposed university data to the CSV file
    with open(filename, mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header row only if the file is empty
        if mode == "w":
            writer.writerow(keys)
        
        # Write corresponding info below each title
        writer.writerows(transposed_data)
        
    print("Data appended to", filename, "file successfully.")

# Main function
def main():
    urls = [     
        "https://www.university-directory.eu/United-States-USA/Athens-State-University.html"
        # Add more URLs here 
    ]
    
    # Use ThreadPoolExecutor to crawl multiple URLs simultaneously
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(crawl_and_extract, urls)
    
    # Filter out None results
    results = [result for result in results if result]
    
    if not results:
        print("No data to write to CSV.")
        return
    
    # Write the data to the existing CSV file
    write_to_csv(results, "universitiestest.csv")

if __name__ == "__main__":
    main()
