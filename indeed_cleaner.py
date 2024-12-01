# Indeed Job Cleaner
# Brett Palmer and Monica Agneta

import pandas as pd
import re 
import  math

df = pd.read_csv('indeed_jobs.csv')
df = df.drop(df.columns[0], axis=1)

for index in df.index:
    salary = df["salary"][index]
    if isinstance(salary, str):
        salary = salary.replace(",","")
        if "-" in salary:
            salary_range = salary.split("-")
            lower_salary = int(re.sub("\D", "", salary_range[0]))
            upper_salary = int(re.sub("\D", "", salary_range[1]))
            avg_salary = (lower_salary + upper_salary)/2
        else:
            avg_salary = int(re.sub("\D", "", salary))
        if "a year" in salary:
            yearly_salary = avg_salary
        elif "an hour" in salary:
            yearly_salary = avg_salary * 40 * 52
        else:
            yearly_salary = None
        df.at[index, 'salary'] = yearly_salary

df.to_csv('indeed_jobs_cleaned.csv')
