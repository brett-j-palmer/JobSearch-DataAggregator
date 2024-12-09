# Indeed Job Scraper
# Brett Palmer and Monica Agneta

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
import pandas as pd
#import requests
import random
import requests
import time
import re 


# Selenium Setup
service = Service(executable_path="/Users/BrettPalmer/Desktop/COS482/ChromeDriver2/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--start-maximized")

user_agents = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
]
user_agent = random.choice(user_agents)
options.add_argument(f"user-agent={user_agent}")

# Create driver instance
driver = webdriver.Chrome(service=service, options=options)



# Stealth settings
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)


job = "software+engineer"
location = "Boston%2C+MA"
radius = "25"

url = f"https://www.indeed.com/jobs?q={job}&l={location}&radius={radius}"
driver.set_window_size(1200, 1000)
driver.get(url)
time.sleep(random.uniform(2, 6)) # Allow 3 seconds for the webpage to open
scroll_pause_time = 3
screen_height = driver.execute_script("return window.screen.height;")

# Wait for the page to load
WebDriverWait(driver, 30).until(
    lambda s: s.find_element(By.ID, "mosaic-jobResults").is_displayed()
)
print("found")

data = [] # 2D list with lists of title, company salary, location,

while True:
    scroll_position =0
    # time.sleep(random.uniform(5, 15))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    for job in soup.select("div.job_seen_beacon"):
        # time.sleep(random.uniform(2,4))
        scroll_position += random.randint(300, 600)
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        title_selector = "h2" 
        company_selector = "span[data-testid='company-name']"
        location_selector = "div[data-testid='text-location']"
        salary_selector = "div.salary-snippet-container"
        link_selector = "a"
        
        link = job.select_one(link_selector)['href']
        
        job_data = []
        job_data.append(job.select_one(title_selector).text)
        job_data.append(job.select_one(company_selector).text)
        job_data.append(job.select_one(location_selector).text)
        salary = job.select_one(salary_selector)
        if salary: 
            job_data.append(salary.text)
        else:
            job_data.append(None)
        job_data.append("https://www.indeed.com" + link)


        print(job_data)
        data.append(job_data)

     # Wait 10 seconds for a load next button, exit if there isn't one
    try:
        WebDriverWait(driver, 10).until(
            lambda s: s.find_element(By.CSS_SELECTOR, 
                'a[data-dd-action-name="next-page"]').is_displayed()  
        )
        print("next button found")
    except TimeoutException:
        break

    # Navigate to the next page if the button is present
    load_more = driver.find_element(By.CSS_SELECTOR, 'a[data-dd-action-name="next-page"]')
    if load_more: driver.execute_script("arguments[0].click();", load_more)

    # # Wait 10 seconds for a load next button, exit if there isn't one
    # try:
    #     WebDriverWait(driver, 10).until(
    #         lambda s: s.find_element(By.CSS_SELECTOR, 
    #             'a[data-testid="pagination-page-next"]').is_displayed()  
    #     )
    #     print("next button found")
    # except TimeoutException:
    #     break

    # # Navigate to the next page if the button is present
    # load_more = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
    # if load_more: driver.execute_script("arguments[0].click();", load_more)


    # next_page = driver.find_element(By.CSS_SELECTOR, 'a[data-dd-action-name="next-page"]')
    # if next_page:
    #     next_page.click()
    #     time.sleep(random.uniform(3, 7))  # Random delay to avoid detection
    #     print(f"Page {start // 10 + 1} loaded.")
    #     start += 10
    # else:
    #     print("Reached the last page.")
    #     break

# Convert 2D list of article information into a dataframe
df = pd.DataFrame(data, columns=['title', 'company', 'location', 'salary', 'link'])

# Save the raw article information to a csv file
df.to_csv('indeed_jobs.csv')