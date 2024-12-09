import os

# Get job, location, and radius from the user
job = input("What job are you looking for? \n e.g.: 'Software Engineer'  ")
location = input("Where are you looking to work? \n e.g.: 'Boston,MA'  ")
radius = input("How many miles from your location would you work? \m e.g.: '5'  ")

# Scrape jobs from Indeed
os.system(f'python indeed_scraper.py "{job}" "{location}"')

# Clean the Indeed jobs
os.system(f'python indeed_cleaner.py')

# os.system(f'python glassdoor_scraper.py "{job}" "{location}" "{radius}"')

# os.system(f'python glassdoor_cleaner.py')