import os
import csv
import time
import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from concurrent.futures import ThreadPoolExecutor

# Function to crawl the webpage and extract university data
def crawl_and_extract(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-features=Permissions-Policy')
    
    # Initialize WebDriver using undetected_chromedriver
    driver = uc.Chrome(options=chrome_options)
    
    try:
        # Add custom headers
        driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        })
        
        # Open the URL
        driver.get(url)
        
        # Wait for the elements to be loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'partner partnermiddle'))
        )
        
        # Find all elements with class "partner partnermiddle"
        course_details = driver.find_elements(By.CLASS_NAME, 'partner partnermiddle')
        
        course_data = []
        
        for detail in course_details:
            try:
                # Find the first <a> tag within each "partner_div" and extract the text within it
                first_a_tag = detail.find_element(By.TAG_NAME, 'a')
                if first_a_tag and "Central Connecticut State University" not in first_a_tag.text:
                    course_data.append({"Course Title": first_a_tag.text.strip()})
            except NoSuchElementException:
                continue
        
        return course_data
    
    except TimeoutException:
        print("Timeout while fetching page:", url)
        return []
    
    finally:
        driver.quit()

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
    
    # Flatten the list of lists and filter out any empty results
    all_courses = [course for result in results for course in result if result]
    
    if all_courses:
        # Write the data to the existing CSV file
        write_to_csv(all_courses, "coursedata.csv")
    else:
        print("No data to write to CSV.")

if __name__ == "__main__":
    main()
