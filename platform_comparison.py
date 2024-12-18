
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

def count_job_platforms(filename):
    # platform counters
    platform_counts = {
        'G': 0,  
        'I': 0  
    }
    
    keyword_platform_counts = {
        'G': 0,  
        'I': 0  
    }

    keywords = ['software engineer', 'software developer', 'programming', 'software development']
    
    try:
       
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.DictReader(csvfile)
            
            for row in csvreader:
                platform = row['platform']
                
                if platform in platform_counts:
                    platform_counts[platform] += 1
                
                title = row['title'].lower()
                
                if any(keyword in title for keyword in keywords):
                    if platform in keyword_platform_counts:
                        keyword_platform_counts[platform] += 1
    
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        return None, None
    except KeyError as e:
        print(f"Error: Missing column in CSV file - {e}")
        return None, None
    
    return platform_counts, keyword_platform_counts

def main():
    filename = 'all_jobs.csv'
    
    total_counts, keyword_counts = count_job_platforms(filename)
    keyword_percentages = {}

    if total_counts and keyword_counts:
        print("Job Count of Each Platform:")
        for platform, total in total_counts.items():
            print(f"Platform {platform}: Total Jobs = {total}")
        
        print("\nRelevant Job Count:")
        for platform, count in keyword_counts.items():
            # calculate percentages
            keyword_percentages[platform] = (count / total_counts[platform]) * 100 if total_counts[platform] > 0 else 0
            print(f"Platform {platform}: Keyword Jobs = {count}, Percentage = {keyword_percentages[platform]:.2f}%")
    
    os.makedirs("images", exist_ok=True) 

    colors = ["green", "blue"]

    # Make a bar graph of average salaries
    df = pd.read_csv("all_jobs.csv") 
    df_avg = df.groupby("platform")["salary"].mean()
    df_avg.plot(kind="bar", title= "Average Salaries By Platform", color=colors)
    plt.xticks(rotation=0)
    plt.xlabel("Platforms")
    plt.ylabel("Average Salaries")
    plt.savefig("images/salaries_avg.png")
    plt.close()

    print("\nAverage Salaries:")
    for platform, avg_salary in df_avg.items():
        print(f"Platform {platform}: Average Salary = {avg_salary:.2f}")

    # Make a histogram of average salaries
    platforms = {
        "Glassdoor": ("G", "green"),
        "Indeed": ("I", "blue")
    }
    plt.figure(figsize=(16, 6))
    for i, (platform_name, (platform_code, color)) in enumerate(platforms.items(), start=1):
        platform_salaries = df[df["platform"] == platform_code]["salary"]
        
        plt.subplot(1, 2, i)
        platform_salaries.plot(kind="hist", bins=15, color=color, alpha=0.7, density=True)
        plt.title(f"{platform_name} Salary Distribution")
        plt.xlabel("Salary")
        plt.ylabel("Frequency")
    plt.savefig("images/salaries_hist.png")
    plt.close()

    # Make a bar graph of total job counts
    plt.bar(total_counts.keys(), total_counts.values(), color=colors)
    plt.title("Job Counts By Platform")
    plt.xlabel("Platforms")
    plt.ylabel("Number of Jobs")
    plt.savefig("images/counts.png")
    plt.close()

    # Make a bar graph of relevancy by percent of keywords found
    plt.bar(keyword_counts.keys(), keyword_percentages.values(), color=colors)
    plt.title("Relevancy By Platform")
    plt.xlabel("Platforms")
    plt.ylabel("% of Jobs Containing Keywords")
    plt.savefig("images/percentages.png")
    plt.close()


    

if __name__ == "__main__":
    main()