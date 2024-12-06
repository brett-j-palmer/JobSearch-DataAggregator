'''
Monica Agneta & Brett Palmer
-Glassdoor job cleaner, means salary and removes duplicates
'''

import pandas as pd
import re
import math


df = pd.read_csv('glassdoor_jobs.csv')

# remove duplicates
df = df.drop_duplicates()

# clean salary
for index in df.index:
    salary = df["salary"][index]
    if isinstance(salary, str):
        print(salary, end="  ")
        salary = salary.replace(",","")
        
        
        if salary == "Not available":
            print("Not Available")
            continue
        
        # remove text from salary
        salary = re.sub(r'\s*\(.*\)', '', salary)
        
        if "-" in salary:
            salary_range = salary.split("-")
            lower_salary = int(re.sub("\D", "", salary_range[0]))
            upper_salary = int(re.sub("\D", "", salary_range[1]))
            avg_salary = (lower_salary + upper_salary)/2
        else:
            try:
                avg_salary = int(re.sub("\D", "", salary))
            except ValueError:
                print(f"Could not parse: {salary}")
                continue
        
        # ensure salary in thousands
        if avg_salary < 1000:
            avg_salary *= 1000
        
        if "Per Hour" in salary:
            # hourly to yearly calculation
            yearly_salary = avg_salary * 40 * 52 / 100
        else:
            yearly_salary = avg_salary
        
        df.at[index, 'salary'] = yearly_salary
        print(yearly_salary)

df.to_csv('glassdoor_jobs_cleaned.csv', index=False)