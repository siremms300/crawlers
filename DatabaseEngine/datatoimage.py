from selenium import webdriver
from PIL import Image

# Function to take screenshot
def take_screenshot(url, save_path):
    # Set up Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # Run Chrome in headless mode
    driver = webdriver.Chrome(options=options)
    
    # Visit the webpage
    driver.get(url)
    
    # Take screenshot
    driver.save_screenshot(save_path)
    
    # Close the webdriver
    driver.quit()

# Example usage
url = "https://www.university-directory.eu/United-States-USA/Air-University-Maxwell-Gunter-Air-Force-Base-Montgomery--Alabama.html"

save_path = "screenshot.png"
take_screenshot(url, save_path)
