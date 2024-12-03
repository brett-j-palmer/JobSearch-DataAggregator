from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time
import pandas as pd
import random

# # Setup Proxies (if available)
# proxies = [
#     "http://proxy1:port",  # Replace with actual proxy
#     "http://proxy2:port",
# ]
# proxy = random.choice(proxies)

# Selenium Setup
service = Service(executable_path="/Users/BrettPalmer/Desktop/COS482/ChromeDriver2/chromedriver")
options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument(f"--proxy-server={proxy}")  # Use proxy
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument(f"user-agent={random.choice(['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',])}")
options.add_argument(f"--window-size={random.randint(800, 1920)},{random.randint(600, 1080)}")  # Random viewport

# Create driver instance
driver = webdriver.Chrome(service=service, options=options)



# Stealth settings
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True)

job = "software+engineer"
location = "Boston%2C+MA"
radius = "5"
url = f"https://www.indeed.com/jobs?q={job}&l={location}&radius={radius}"

try:
    driver.get(url)
    WebDriverWait(driver, 10).until(
        lambda s: s.find_element(By.ID, "mosaic-jobResults").is_displayed()
    )
    print("Page loaded.")
except TimeoutException:
    print("Failed to load page. Retrying...")
    driver.quit()

data = []
scroll_pause_time = random.uniform(2, 4)
scroll_position = 0

# Simulate human-like scrolling and random actions
for _ in range(50):
    scroll_position += random.randint(200, 400)
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    time.sleep(scroll_pause_time + random.uniform(1, 3))

    action = ActionChains(driver)
    action.move_by_offset(random.randint(0, 200), random.randint(0, 200)).perform()  # Random mouse movement
    action.reset_actions()

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    for job in soup.select("div.job_seen_beacon"):
        try:
            title = job.select_one("h2").text
            company = job.select_one("span[data-testid='company-name']").text
            location = job.select_one("div[data-testid='text-location']").text
            salary = job.select_one("div.salary-snippet-container")
            link = job.select_one("a")['href']

            data.append([title, company, location, salary.text if salary else None, f"https://www.indeed.com{link}"])
        except AttributeError:
            continue

    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]').is_displayed()
        )
        next_button = driver.find_element(By.CSS_SELECTOR, 'a[data-testid="pagination-page-next"]')
        driver.execute_script("arguments[0].click();", next_button)
        time.sleep(random.uniform(3, 6))
    except TimeoutException:
        break

driver.quit()

# Convert list to DataFrame and save
df = pd.DataFrame(data, columns=['title', 'company', 'location', 'salary', 'link'])
df.to_csv('indeed_jobs.csv', index=False)
print("Scraping complete. Data saved.")
