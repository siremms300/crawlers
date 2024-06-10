# import requests
# from bs4 import BeautifulSoup

# # URL of the page to scrape
# url = "https://www.university-directory.eu/js/createpage.php?view=showJobs&jobtyp=5&jtyp=0&type=Courses-Programs-Degrees&university=Air+University+%28Maxwell-Gunter+Air+Force+Base+Montgomery%2C+Alabama%29&country=US&sid=10437&jobtypes=5&countries=US&page=1"

# # Headers to mimic a browser request
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
# }

# # Send a GET request to the URL with headers
# response = requests.get(url, headers=headers)

# # Parse the HTML content
# soup = BeautifulSoup(response.content, "html.parser")

# # Find all <div> with class "partner partnermiddle"
# partner_divs = soup.find_all("div", class_="partner partnermiddle")

# # Find all <a> tags within each "partner_div" and extract the text within them
# # if partner_divs:
# #     for partner_div in partner_divs:
# #         for a_tag in partner_div.find_all("a"):
# #             print(a_tag.text.strip())

# if partner_divs:
#     for partner_div in partner_divs:
#         first_a_tag = partner_div.find("a")
#         if first_a_tag:
#             print(first_a_tag.text.strip())
# else:
#     print("No <div class='partner partnermiddle'> found on the page.")







import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://www.university-directory.eu/js/createpage.php?view=showJobs&jobtyp=5&jtyp=0&type=Courses-Programs-Degrees&university=Air+University+%28Maxwell-Gunter+Air+Force+Base+Montgomery%2C+Alabama%29&country=US&sid=10437&jobtypes=5&countries=US&page=1"

# Headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
}

# Send a GET request to the URL with headers
response = requests.get(url, headers=headers)

# Parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all <div> with class "partner partnermiddle"
partner_divs = soup.find_all("div", class_="partner partnermiddle")

# Find the first <a> tag within each "partner_div" and extract the text within it
if partner_divs:
    for partner_div in partner_divs:
        first_a_tag = partner_div.find("a")
        if first_a_tag and "Air University (Maxwell-Gunter Air Force Base Montgomery, Alabama)" not in first_a_tag.text:
            print(first_a_tag.text.strip())
else:
    print("No <div class='partner partnermiddle'> found on the page.")


