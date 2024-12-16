
import csv

def count_job_platforms(filename):
    # platform counters
    platform_counts = {
        'I': 0,  
        'G': 0  
    }
    
    keyword_platform_counts = {
        'I': 0,  
        'G': 0  
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
    
    if total_counts and keyword_counts:
        print("Job Count of Each Platform:")
        for platform, total in total_counts.items():
            print(f"Platform {platform}: Total Jobs = {total}")
        
        print("\nRelevant Job Count:")
        for platform, count in keyword_counts.items():
            # calculate percentages
            percentage = (count / total_counts[platform]) * 100 if total_counts[platform] > 0 else 0
            print(f"Platform {platform}: Keyword Jobs = {count}, Percentage = {percentage:.2f}%")

if __name__ == "__main__":
    main()