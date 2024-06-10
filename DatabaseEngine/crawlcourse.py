import os.path
import requests
from bs4 import BeautifulSoup
import csv
import random
import time
from concurrent.futures import ThreadPoolExecutor

# List of user-agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
]


# Function to crawl the webpage and extract university data
def crawl_and_extract(url):
    # Rotate user-agent
    headers = {
        'User-Agent': random.choice(user_agents),
    }
    
    try:
        # Send a GET request to the URL with headers and proxy
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all <div> tags with class "partner partnermiddle"
            course_details = soup.find_all('div', class_='partner partnermiddle')
            
            course_data = []
            
            for detail in course_details:
                # Find the first <a> tag within each "partner_div" and extract the text within it
                first_a_tag = detail.find("a")
                if first_a_tag and "Central Connecticut State University" not in first_a_tag.text:
                    course_data.append({"Course Title": first_a_tag.text.strip()})
            
            return course_data
        
        else:
            print("Failed to fetch page:", response.status_code)
            return None
    except Exception as e:
        print(f"Error fetching page {url}: {e}")
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
        writer = csv.DictWriter(csvfile, fieldnames=["Course Title"])
        
        # Write the header row only if the file is empty
        if mode == "w":
            writer.writeheader()
        
        # Write the course data to the CSV file
        writer.writerows(data)
        
    print("Data appended to", filename, "file successfully.")

# Main function
def main():
    urls = [
        "https://www.university-directory.eu/js/createpage.php?view=showJobs&jobtyp=5&jtyp=0&type=Courses-Programs-Degrees&university=Central+Connecticut+State+University&country=US&sid=6239&jobtypes=5&countries=US&page=1",
        "https://www.university-directory.eu/js/createpage.php?view=showJobs&jobtyp=5&jtyp=0&type=Courses-Programs-Degrees&university=Central+Connecticut+State+University&country=US&sid=6239&jobtypes=5&countries=US&page=2",
        "https://www.university-directory.eu/js/createpage.php?view=showJobs&jobtyp=5&jtyp=0&type=Courses-Programs-Degrees&university=Central+Connecticut+State+University&country=US&sid=6239&jobtypes=5&countries=US&page=3",
        "https://www.university-directory.eu/js/createpage.php?view=showJobs&jobtyp=5&jtyp=0&type=Courses-Programs-Degrees&university=Central+Connecticut+State+University&country=US&sid=6239&jobtypes=5&countries=US&page=4",
    ]
    
    # Use ThreadPoolExecutor to crawl multiple URLs simultaneously
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(crawl_and_extract, urls)
    
    # Filter out None results
    results = [result for result in results if result]
    
    if results:
        # Write the data to the existing CSV file
        write_to_csv([course for result in results for course in result], "coursedata.csv")
    else:
        print("No data to write to CSV.")

if __name__ == "__main__":
    main()
