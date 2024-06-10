import os.path
import requests
from bs4 import BeautifulSoup
import csv
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin

# Function to crawl the webpage and extract university data
def crawl_and_extract(url):
    # Add headers to the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    }
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the h3 strong tag with text "Unspecified"
        unspecified_tag = soup.find('a', string='Adams State College')
        if unspecified_tag:
            # Get the parent <a> tag's href attribute
            parent_a_tag = unspecified_tag.find_parent('a')
            if parent_a_tag and 'href' in parent_a_tag.attrs:
                # Construct the absolute URL from the relative URL
                unspecified_url = urljoin(url, parent_a_tag['href'])
                
                # Now, crawl the URLs within the unspecified URL
                return crawl_url(unspecified_url)
            else:
                print("No link found within the 'Unspecified' section.")
        else:
            print("No 'Unspecified' section found.")
            
    else:
        print("Failed to fetch page:", response.status_code)
        return None

# Function to crawl URLs within a page
def crawl_url(url):
    # Add headers to the request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36'
    }
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <a> tags
        links = soup.find_all('a', href=True)
        
        # Extract URLs from the href attributes
        extracted_urls = [link['href'] for link in links]
        
        # Filter out external URLs
        internal_urls = [link for link in extracted_urls if link.startswith('/')]
        
        return internal_urls
    
    else:
        print("Failed to fetch page:", response.status_code)
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
    
    # Write the data to the CSV file
    with open(filename, mode, newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["URL"])
        
        # Write the header row only if the file is empty
        if mode == "w":
            writer.writeheader()
        
        # Write the URL data to the CSV file
        writer.writerows([{"URL": url} for url in data])
        
    print("Data appended to", filename, "file successfully.")

# Main function
def main():
    seed_url = "https://www.university-directory.eu/United-States-USA/Adams-State-College.html"
    
    # Crawl and extract URLs from the seed URL
    internal_urls = crawl_and_extract(seed_url)
    
    if internal_urls:
        # Write the data to the existing CSV file
        write_to_csv(internal_urls, "crawled_urls.csv")
    else:
        print("No data to write to CSV.")

if __name__ == "__main__":
    main()
