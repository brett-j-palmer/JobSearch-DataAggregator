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

service = Service(executable_path=r"C:\Users\12075\Desktop\482\chromedriver-win64\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging', "enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.glassdoor.com/Job/boston-software-engineer-jobs-SRCH_IL.0,6_IC1154532_KO7,24.htm")

job_data = []

def close_signup_modal():
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[alt='Close']"))
        )
        close_button.click()
    except:
        pass

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.JobCard_jobCardContainer__arQlW"))
)
close_signup_modal()

scroll_pause_time = 3
scroll_position = 0

for page_num in range(1, 31):  
    try:
        # scroll page
        scroll_position += random.randint(200, 400)
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(scroll_pause_time + random.uniform(0, 2))
        
        # find all jobs on page
        jobs = driver.find_elements(By.CSS_SELECTOR, "div.JobCard_jobCardContainer__arQlW")
        print(f"Found {len(jobs)} jobs on page {page_num}")
        
        for job in jobs:
            try:
                # Get job title
                try:
                    title = job.find_element(By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1").text
                except NoSuchElementException:
                    title = "N/A"
                
                # Get company name
                try:
                    company = job.find_element(By.CSS_SELECTOR, "span.EmployerProfile_compactEmployerName__9MGcV").text
                except NoSuchElementException:
                    company = "N/A"
                
                # Get salary information
                try:
                    salary = job.find_element(By.CSS_SELECTOR, "div.JobCard_salaryEstimate__QpbTW").text
                except NoSuchElementException:
                    salary = "Not available"
                
                # Get location
                try:
                    location = job.find_element(By.CSS_SELECTOR, "div.JobCard_location__Ds1fM").text
                except NoSuchElementException:
                    location = "N/A"
                
                # Get job link
                try:
                    link = job.find_element(By.CSS_SELECTOR, "a.JobCard_jobTitle__GLyJ1").get_attribute('href')
                except NoSuchElementException:
                    link = "N/A"

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
        
        # load more jobs
        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[@class='button_ButtonContent__a4TUW']//span[text()='Show more jobs']"))
            )
            driver.execute_script("arguments[0].click();", next_button.find_element(By.XPATH, '..'))
            
            print(f"Moving to page {page_num + 1}")
            
            time.sleep(random.uniform(3, 10))
            
            close_signup_modal()
            
        except TimeoutException:
            print(f"No more pages to load at page {page_num}")
            break
            
    except Exception as e:
        print(f"Error on page {page_num}: {e}")
        break

df = pd.DataFrame(job_data)
df.to_csv("glassdoor_jobs.csv", index=False)

driver.quit()