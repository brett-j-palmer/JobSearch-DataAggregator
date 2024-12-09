# Indeed Job Scraper
# Brett Palmer and Monica Agneta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import random
import json
import sys

# Get path to driver from configuration file
with open("config.json", "r") as f:
    config = json.load(f)
data_path = config["data_path"]

# # Get job, location, and radius from the user
# job = input("What job are you looking for? \n e.g.: 'Software Engineer'  ")
# job = "+".join(job.split())
# location = input("Where are you looking to work? \n e.g.: 'Boston, MA'  ")
# location = "%2C+".join(location.replace(",", "").split())
# radius = input("How many miles from your location would you work? \m e.g.: '5'  ")

if len(sys.argv)>1:
    job = sys.argv[1]
else:
    job = input("What job are you looking for? \n e.g.: 'Software Engineer'  ")
job = "+".join(job.split())

if len(sys.argv)>2:
    location = sys.argv[2]
else:
    location = input("Where are you looking to work? \n e.g.: 'Boston, MA'  ")
location = "%2C".join(location.replace(" ","").split(","))

if len(sys.argv)>3:
    radius = sys.argv[3]
else:
    radius = input("How many miles from your location would you work? \n e.g.: '5'  ")

# Construct a url for the user's Indeed search
base_url = f"https://www.indeed.com/jobs?q={job}&l={location}&radius={radius}&start="

# Use mobile user agents to avoid getting blocked by CloudFare
user_agents = [
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]

# Selenium Setup
def setup_driver():
    user_agent = random.choice(user_agents) # Randomize User-Agent
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--incognito")
    # Return a driver instance
    return webdriver.Chrome(service=Service(data_path), options=options)

# Create driver instance
driver = setup_driver()
# driver.set_window_size(650, 1000)

# job = "software+engineer"
# location = "Boston%2C+MA"
# radius = "5"
# base_url = f"https://www.indeed.com/jobs?q={job}&l={location}&radius={radius}&start="

data = []
start = 0  # Initial start value

i=0
while True:
    i+=1
    #Open the next page
    url = base_url + str(start)
    driver.get(url)

    #Wait a random amount of time to bypass captchas
    time.sleep(random.uniform(1, 2))

    # Wait for the page to load
    try:
        WebDriverWait(driver, 15).until( 
            lambda s: s.find_element(By.ID, "mosaic-jobResults").is_displayed()
        )
        print(f"Page {i+1} loaded.")
    except TimeoutException:  
        print("Breaking, page loading took too long.")
        break
    
    #Click past a popup that sometimes appears
    try:
        continue_button = driver.find_element(By.CSS_SELECTOR, 'button.mosaic-provider-app-download-promos-service-1pe2qp4')
        driver.execute_script("arguments[0].click();", continue_button)
    except NoSuchElementException:  
        pass

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml') 
    
    # time.sleep(1800) 
    for job in soup.select("div.job_seen_beacon"):
        title_selector = "h2"  
        company_selector = "span[data-testid='company-name']"
        location_selector = "div[data-testid='text-location']"
        salary_selector = "div.css-1a6kja7"
        link_selector = "a"

        link = job.select_one(link_selector)['href']
        
        job_data = [
            job.select_one(title_selector).text,
            job.select_one(company_selector).text, 
            job.select_one(location_selector).text,
            job.select_one(salary_selector).text if job.select_one(salary_selector) else None,
            "https://www.indeed.com" + link 
        ]

        # print(job_data)
        data.append(job_data)
    
    # Increment start parameter for the next page
    start += 10

    # Check if is another page to visit, break if not
    if not soup.select_one('a[data-dd-action-name="next-page"]'):
        print("All jobs have been scraped.")
        break

# Convert 2D list of article information into a dataframe
df = pd.DataFrame(data, columns=['title', 'company', 'location', 'salary', 'link'])

# Save the article information to a CSV file
df.to_csv('indeed_jobs.csv', index=False)
driver.quit()