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
job_list = []
# for i in range(9):
# page_index = i + 1
# print('page index', page_index)
url = f"https://www.dice.com/job-detail/0200b094-1654-4165-bffe-da96dff1f689?searchlink=search%2F%3FcountryCode%3DUS%26radius%3D30%26radiusUnit%3Dmi%26page%3D6%26pageSize%3D100%26filters.postedDate%3DSEVEN%26filters.employmentType%3DFULLTIME%26filters.isRemote%3Dtrue%26language%3Den%26eid%3DS2Q_&searchId=68"
print(url)
driver.get(url)


#   # Wait for a few seconds to let the page load (adjust as needed)
time.sleep(15)

#   # Get the page source with the dynamically loaded content
page_source = driver.page_source
#   search_card = driver.find_element(By.TAG_NAME, 'dhi-search-cards-widget')
#   hyper_links = search_card.find_elements(By.TAG_NAME, 'h5')
#   print(type(hyper_links), len(hyper_links))

#   interation = len(hyper_links)

  
#   # while interation > 0:
#   #get
#   for i in range(interation):
#     print('interate', i) 
#     print('hyper_links', hyper_links[i].text)
#     if hyper_links[i].get_attribute('childElementCount') == '1':
#       print('check')
#       job_id = hyper_links[i].find_element(By.TAG_NAME, 'a').get_attribute('id')
#       job_link = hyper_links[i].find_element(By.TAG_NAME, 'a').get_attribute('href')
#       job_title = hyper_links[i].text
#       job_record = {
#         'job_id': job_id,
#         'job_link': job_link,
#         'job_title': job_title
#       }
#       job_list.append(job_record)

# job_index = 0
# for job in job_list:
#   job_index += 1
#   print(job_index, 'run salary job')
#   driver.get(job['job_link'])
#   time.sleep(5)
#   job_skills_section = driver.find_element(By.TAG_NAME, 'section')
#   job_skills_list = job_skills_section.find_elements(By.TAG_NAME, 'li')
#   job_company = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/header/div/div/div[3]/ul/ul[1]/li[1]').text
  
#   job_salary_tag_name = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/header/div/div/div[3]/ul/ul[2]/li[1]/p')
#   print('check', job_salary_tag_name.get_attribute('data-cy'))
#   job_salary = job_salary_tag_name.text if job_salary_tag_name.get_attribute('data-cy') == 'compensationText' else 'Depends on Experience'
#   print('*'*50)
#   job_skills_text = []
#   for skill in job_skills_list:
#     job_skills_text.append(skill.text)
#   job['job_company'] = job_company
#   job['job_salary'] = job_salary
#   job['job_skills'] = ', '.join(job_skills_text)
  
# # # Export to excel
driver.quit()
# pyexcel.save_as(records=job_list, dest_file_name="job-test.xls")

# Close the browser

print('end')

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Convert the BeautifulSoup object to a string
soup_string = str(soup)

# Write the parsed HTML content to a file
with open("_page_test.html", "w", encoding="utf-8") as file:
    file.write(soup_string)

print("Parsed HTML content saved to 'parsed_page.html'")
