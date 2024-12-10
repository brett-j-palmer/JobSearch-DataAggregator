import os
import pandas as pd

# Get job, location, and radius from the user
job = input("What job are you looking for? \n e.g.: 'Software Engineer'  ")
location = input("Where are you looking to work? \n e.g.: 'Boston,MA'  ")
radius = input("How many miles from your location would you work? \n e.g.: '5'  ")

print("\nWe have now created the file top_jobs.csv in your directory \nIt contains information and application links from the top 10 paying jobs we found.")

# # Scrape jobs from Indeed
# os.system(f'python indeed_scraper.py "{job}" "{location}"')

# # Clean the Indeed jobs
# os.system(f'python indeed_cleaner.py')

os.system(f'python glassdoor_scraper.py "{job}" "{location}" "{radius}"')

os.system(f'python glassdoor_cleaner.py')

# Combine the platforms into one
indeed_df = pd.read_csv('indeed_jobs_cleaned.csv')
indeed_df['platform'] = "I"
indeed_average = indeed_df['salary'].mean()
# print(indeed_average)

glassdoor_df = pd.read_csv('glassdoor_jobs_cleaned.csv')
glassdoor_df['platform'] = "G"
glassdoor_average = glassdoor_df['salary'].mean()
# print(glassdoor_average)

combined_df = pd.concat([indeed_df, glassdoor_df], ignore_index=True)
combined_df = combined_df.sort_values(by='salary', ascending=False)
combined_df = combined_df.drop_duplicates(subset=['title', 'company', 'salary', 'location'])
# combined_df = combined_df.drop('link', axis=1)
combined_df.to_csv('all_jobs.csv', index=False)

top_jobs_df = combined_df.head(10)
top_jobs_df.to_csv('top_jobs.csv', index=False)