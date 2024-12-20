'''
Monica Agneta & Brett Palmer
-Glassdoor job scraper
'''
import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome
from selenium.webdriver.common.keys import Keys
import json
import sys

def fetch_search_url(keyword, location, radius):
    driver = Chrome(service=Service(data_path))
    try:
        driver.get("https://www.glassdoor.com/Job/index.htm")
        time.sleep(2)

        job_title_input = driver.find_element(By.ID,"searchBar-jobTitle")
        location_input = driver.find_element(By.ID, "searchBar-location")
        job_title_input.send_keys(keyword)
        location_input.send_keys(location)
        location_input.send_keys(Keys.RETURN)

        time.sleep(2)
        current_url = driver.current_url + "?radius=" + radius
        print("Search URL:", current_url)
        return current_url

    except Exception as e:
        print("Error fetching search URL:" , e)
        return None
    finally:
        driver.quit() 

def close_signup_modal():
    try:
        close_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.CloseButton"))
        )
        close_button.click()
    except:
        pass

with open("config.json", "r") as f:
    config = json.load(f)
data_path = config["data_path"]

if len(sys.argv)>1:
    job = sys.argv[1]
else:
    job = input("What job are you looking for? \n e.g.: 'Software Engineer'  ")
job = job.strip()

if len(sys.argv)>2:
    location = sys.argv[2]
else:
    location = input("Where are you looking to work? \n e.g.: 'Boston, MA'  ")
location = location.strip()

if len(sys.argv)>3:
    radius = sys.argv[3]
else:
    radius = input("How many miles from your location would you work? \n e.g.: '5'  ")
radius = radius.strip()

search_url = fetch_search_url(job, location, radius)
if not search_url:
    print("Failed to fetch search URL. Exiting.")
    exit()

# driver = webdriver.Chrome(service=service, options=options)
driver = Chrome(service=Service(data_path))
driver.get(search_url)

job_data = []

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.JobCard_jobCardContainer__arQlW"))
)
close_signup_modal()

scroll_position = 0
for page_num in range(1, 40):  
    try:
        # scroll page and pause to bypass blockers
        scroll_position += random.randint(200, 400)
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(random.uniform(0,2))
        
        # load more jobs
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='button_ButtonContent__a4TUW']//span[text()='Show more jobs']"))
            )
            driver.execute_script("arguments[0].click();", next_button.find_element(By.XPATH, '..'))
            
            print(f"Moving to page {page_num + 1}")
            
            # time.sleep(random.uniform(1, 3))
            
            close_signup_modal()
            
        except TimeoutException:
            print(f"No more pages to load at page {page_num}")
            break
            
    except Exception as e:
        print(f"Error on page {page_num}: {e}")
        break

# find all jobs on page
jobs = driver.find_elements(By.CSS_SELECTOR, "div.JobCard_jobCardContainer__arQlW")
print(f"Found {len(jobs)} jobs on page {page_num}")

for job in jobs:
    try:
        # Get job title
        try:
            title = job.find_element(By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1").text
        except NoSuchElementException:
            title = None
        
        # Get company name
        try:
            company = job.find_element(By.CSS_SELECTOR, "span.EmployerProfile_compactEmployerName__9MGcV").text
        except NoSuchElementException:
            company = None
        
        # Get salary information
        try:
            salary = job.find_element(By.CSS_SELECTOR, "div.JobCard_salaryEstimate__QpbTW").text
        except NoSuchElementException:
            salary = None
        
        # Get location
        try:
            location = job.find_element(By.CSS_SELECTOR, "div.JobCard_location__Ds1fM").text
        except NoSuchElementException:
            location = None
        
        # Get job link
        try:
            link = job.find_element(By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1").get_attribute('href')
        except NoSuchElementException:
            link = None

        job_info = {
            "title": title,
            "company": company,
            "salary": salary,
            "location": location,
            "link": link
        }
        
        job_data.append(job_info)

        print('Job title:', title)
        print('Company:', company)
        print('Salary:', salary)
        print('Location:', location)
        print('Link:', link)
        print('\n')
        
    except Exception as e:
        print(f"Error extracting job data: {e}")
        continue


df = pd.DataFrame(job_data)
df.to_csv("glassdoor_jobs.csv", index=False)

driver.quit()