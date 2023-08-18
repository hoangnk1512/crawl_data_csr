from pymongo import MongoClient
from bson import ObjectId
from bs4 import BeautifulSoup
from lxml import etree
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import psycopg2
client = MongoClient("mongodb://localhost:27017/")
db = client['data_scraping']
collection = db['data']
chrome_options = Options()
chrome_options.add_argument("--headless")

# Set the path to your downloaded Chrome web driver
chrome_driver_path = "C:\\Users\Dell\Documents\craw\crawl_data_csr\chromedriver.exe"
import json
# URL to scrape

# Initialize the Chrome driver
service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
job_records = collection.find({})
job_list = []
i = 0
for job_record in job_records:
  print(job_record['_id'])
  i += 1
  html_content = job_record['job_page_source']
  
  driver.execute_script("document.children[0].innerHTML = {}".format(json.dumps(html_content)))
  time.sleep(5)
  try:
    job_title = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/header/div/div/h1').text
    job_company = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/header/div/div/div[3]/ul/ul[1]/li[1]').text
    job_salary_tag_name = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/header/div/div/div[3]/ul/ul[2]/li[1]/p')
    job_salary = job_salary_tag_name.text if job_salary_tag_name.get_attribute('data-cy') == 'compensationText' else 'Depends on Experience'
    job_skills_section = driver.find_element(By.TAG_NAME, 'section')
    print(job_skills_section)
    job_skills_ul_tag = job_skills_section.find_element(By.TAG_NAME, 'ul')
    print(job_skills_ul_tag.get_attribute('data-cy'))
    job_skills_list = job_skills_section.find_elements(By.TAG_NAME, 'li') if job_skills_ul_tag.get_attribute('data-cy') == 'skillsList' else []
    job_skills_text = []
    for skill in job_skills_list:
      job_skills_text.append(skill.text)
  except:
    print('*'* 100)
    print('Something error', print(job_record['_id']))
    job_skills_text = []
    job_salary = None
    job_company = None
    job_title = None
  job_record_ = {
    'job_skills': ', '.join(job_skills_text),
    'job_salary': job_salary,
    'job_company': job_company,
    'job_title': job_title,
    'job_link': job_record['job_link']
  }
  job_list.append(job_record_)
  driver.execute_script("document.children[0].innerHTML = ''")


# print(job_list)
driver.quit()

connection = psycopg2.connect(
    host="localhost",
    database="data_scraping",
    user="postgres",
    password="ngochoang123"
)

create_table_query = '''
    CREATE TABLE job_table (
        id SERIAL PRIMARY KEY,
        job_salary VARCHAR(500),
        job_skills VARCHAR(500),
        job_company VARCHAR(500),
        job_title VARCHAR(500),
        job_link VARCHAR(500) UNIQUE
    )
'''
cursor = connection.cursor()

for job_record in job_list:
  data_to_upsert = [(str(job_record['job_salary']), str(job_record['job_skills']), str(job_record['job_company']), str(job_record['job_title']), str(job_record['job_link']))]
  upsert_query = '''
      INSERT INTO job_table (job_salary, job_skills, job_company, job_title, job_link)
      VALUES %s
      ON CONFLICT (job_link) DO UPDATE
      SET job_salary = EXCLUDED.job_salary,
          job_skills = EXCLUDED.job_skills,
          job_company = EXCLUDED.job_company,
          job_title = EXCLUDED.job_title;
  '''
  # cursor.execute(create_table_query)

  cursor.execute(upsert_query, data_to_upsert)
connection.commit()
cursor.close()
connection.close()
