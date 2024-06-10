import requests
from bs4 import BeautifulSoup
import csv

# Function to crawl href attributes under h3 elements and store them in a CSV file
def crawl_href(url, output_file):
    try:
        # Set User-Agent header to mimic a web browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        # Send a GET request to the URL with headers
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all h3 elements
        h3_elements = soup.find_all('h3')

        # Open CSV file in write mode
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Href'])

            # Loop through each h3 element
            for h3 in h3_elements:
                # Find the anchor tag within the h3 element
                a_tag = h3.find('a')

                # If anchor tag is found, write its href attribute to the CSV file
                if a_tag:
                    href = a_tag.get('href')
                    writer.writerow([href])
                    print(href)

        print("Data saved to", output_file)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    url = 'https://www.university-directory.eu/USA/Wyoming'  # Replace this with the URL you want to crawl
    output_file = 'href_data.csv'  # CSV file to store the data
    print("Href attributes under h3 elements:")
    crawl_href(url, output_file)
