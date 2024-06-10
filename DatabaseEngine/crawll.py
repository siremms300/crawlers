import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor

# Function to crawl the webpage and extract university names
def crawl_and_extract(url):
    # Add headers to the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <h3> tags containing university names
        university_tags = soup.find_all('h3')
        
        # Extract university names from the <h3> tags
        university_names = [tag.text.strip() for tag in university_tags]
        
        return university_names
    else:
        print("Failed to fetch page:", response.status_code)
        return None

# Main function
def main():
    urls = [
        # "https://www.university-directory.eu/USA/Virginia",
        "https://www.university-directory.eu/USA/Wisconsin",
        "https://www.university-directory.eu/USA/Wyoming",
        # Add more URLs here
    ]
    
    # Use ThreadPoolExecutor to crawl multiple URLs simultaneously
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(crawl_and_extract, urls)
    
    # Append the extracted university names to the existing CSV file
    with open("universities.csv", "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        for universities in results:
            if universities:
                for name in universities:
                    writer.writerow([name])
        
    print("Data appended to universities.csv file successfully.")

if __name__ == "__main__":
    main()
