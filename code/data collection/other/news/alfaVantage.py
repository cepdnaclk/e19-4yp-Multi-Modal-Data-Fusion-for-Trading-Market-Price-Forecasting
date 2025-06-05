import requests
import json

# Your Alpha Vantage API key
API_KEY = 'RQW3P955G1RBTWQW'

# Alpha Vantage News endpoint
news_url = f'https://www.alphavantage.co/query'

# Fetch financial news
def fetch_financial_news():
    params = {
        'function': 'NEWS_SENTIMENT',
        'apikey': API_KEY
    }
    response = requests.get(news_url, params=params)
    news_data = response.json()

    # Print the raw data from API
    print("Raw API Response:")
    print(json.dumps(news_data, indent=2))  # Pretty-print the raw response

    if 'data' not in news_data:
        print(f"No news available.")
        return

    for idx, article in enumerate(news_data['data'], start=1):
        print(f"Article {idx}:")
        print(f"Title: {article.get('title', 'No title available')}")
        print(f"Source: {article.get('source', 'No source')}")
        print(f"Published: {article.get('time', 'No date available')}")
        print(f"URL: {article.get('url', 'No URL available')}")
        print(f"Summary: {article.get('summary', 'No summary available')}")
        print("-------")

# Example usage: Fetch financial news
fetch_financial_news()
