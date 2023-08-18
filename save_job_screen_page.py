from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client['data_scraping']
collection = db['job_page']

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyexcel
from datetime import datetime

# Set up Chrome options to run headless
chrome_options = Options()
chrome_options.add_argument("--headless")

# Set the path to your downloaded Chrome web driver
chrome_driver_path = "C:\\Users\Dell\Documents\craw\crawl_data_csr\chromedriver.exe"

# URL to scrape

# Initialize the Chrome driver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the URL
page_list = []
for i in range(9):
  page_index = i + 1
  print('page index', page_index)
  url = f"https://www.dice.com/jobs?countryCode=US&radius=30&radiusUnit=mi&page={page_index}&pageSize=100&filters.postedDate=SEVEN&filters.employmentType=FULLTIME&filters.isRemote=true&language=en&eid=S2Q_,Sg_1"
  print(url)
  driver.get(url)


  # Wait for a few seconds to let the page load (adjust as needed)
  time.sleep(15)
  soup = BeautifulSoup(driver.page_source, "html.parser")
  soup_string = str(soup)
  # Get the page source with the dynamically loaded content
  page_source = driver.page_source
  page_list.append({
    'page_index': page_index,
    'page_source': soup_string,
    'natural_id':str(datetime.now()) + url,
    'date': datetime.now()
  })
  
driver.quit()

for page in page_list:
  collection.update_one({'natural_id': page['natural_id']}, {'$set': page}, upsert=True)


print('end')


