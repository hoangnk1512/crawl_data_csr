from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service

# Set up Chrome options to run headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Set the path to your downloaded Chrome web driver
chrome_driver_path = "D:\Mind-task\crawl_data\crawl_data\chromedriver.exe"

# URL to scrape
url = "https://www.dice.com/jobs?countryCode=US&radius=30&radiusUnit=mi&page=1&pageSize=100&filters.postedDate=SEVEN&filters.employmentType=FULLTIME&filters.isRemote=true&language=en&eid=S2Q_,Sg_1"

# Initialize the Chrome driver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the URL
driver.get(url)

# Wait for a few seconds to let the page load (adjust as needed)
time.sleep(5)

# Get the page source with the dynamically loaded content
page_source = driver.page_source

# Close the browser
driver.quit()

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Convert the BeautifulSoup object to a string
soup_string = str(soup)

# Write the parsed HTML content to a file
with open("parsed_page.html", "w", encoding="utf-8") as file:
    file.write(soup_string)

print("Parsed HTML content saved to 'parsed_page.html'")
