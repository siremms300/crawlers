import requests
from bs4 import BeautifulSoup
import random

# URL of the site to crawl
url = 'https://worlduniversitydirectory.com/edu/directory/?dir=University&country=United+States'

# List of User-Agent strings
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
]

# Select a random User-Agent
headers = {
    'User-Agent': random.choice(user_agents),
    'Referer': 'https://www.google.com/',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'DNT': '1'  # Do Not Track Request Header
}

# Proxy configuration

# Use a session to maintain headers and cookies
session = requests.Session()
session.headers.update(headers)

# Make a request to the website using the proxy
response = session.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all h3 elements
    h3_elements = soup.find_all('h3')
    
    # Print the h3 elements
    for h3 in h3_elements:
        print(h3.text)
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
