# Indeed Job Cleaner
# Brett Palmer and Monica Agneta

import pandas as pd

df = pd.read_csv('indeed_jobs.csv')
df = df.drop_duplicates()
# df = df.drop(df.columns[0], axis=1)

for index in df.index:
    salary = df["salary"][index]
    if isinstance(salary, str):
        # print(salary, end="  ")
        salary = salary.replace(",","")
        if "-" in salary:
            salary_range = salary.split("-")
            lower_salary = float("".join([char for char in salary_range[0] if (char.isdigit() or char==".")] ))
            upper_salary = float("".join([char for char in salary_range[1] if (char.isdigit() or char==".")] ))
            avg_salary = (lower_salary + upper_salary)/2
        else:
            avg_salary = float("".join([char for char in salary if (char.isdigit() or char==".")] ))
        if "a year" in salary:
            yearly_salary = avg_salary
        elif "an hour" in salary:
            yearly_salary = avg_salary * 40 * 52
        else:
            yearly_salary = None
        yearly_salary = round(yearly_salary,2)
        df.at[index, 'salary'] = yearly_salary
        # print(yearly_salary)

df.to_csv('indeed_jobs_cleaned.csv', index=False)
