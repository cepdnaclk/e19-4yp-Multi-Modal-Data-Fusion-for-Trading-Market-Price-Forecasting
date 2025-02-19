import requests
import csv
from datetime import datetime, timedelta

# Get your API key from https://newsapi.org/
api_key = "8dd734e5d7b54fc48b1f25828a777272"
url = "https://newsapi.org/v2/everything"

# Define the time range: past 30 days
to_date = datetime.now().strftime('%Y-%m-%d')
from_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

params = {
    "q": "finance",  # search for finance-related news
    "from": from_date,  # Set to date 30 days ago
    "to": to_date,      # Set to current date
    "apiKey": api_key,  # Your News API key
    "pageSize": 100     # Number of results per request
}

# Make API request
response = requests.get(url, params=params)
data = response.json()

# Check if the request was successful
if response.status_code == 200:
    # Check if we have articles
    if "articles" in data:
        # Open a CSV file for writing
        with open('financial_news.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write the header row
            writer.writerow(["Title", "Published At", "Source", "URL"])
            
            # Write article data
            for article in data["articles"]:
                writer.writerow([
                    article['title'],
                    article['publishedAt'],
                    article['source']['name'],
                    article['url']
                ])
        print("Data saved to financial_news.csv")
    else:
        print("No articles found.")
else:
    print(f"Error: {data.get('message', 'Something went wrong')}")
