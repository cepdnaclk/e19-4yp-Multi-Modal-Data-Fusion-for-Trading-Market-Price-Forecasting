from yahooquery import Ticker

# Function to fetch news related to a symbol
def fetch_gold_news():
    # Symbols related to gold
    symbols = ["GC=F", "GLD", "XAUUSD=X"]
    
    for symbol in symbols:
        print(f"Fetching news for {symbol}...")
        
        # Use yahooquery's Ticker object to fetch news for the symbol
        try:
            ticker = Ticker(symbol)
            news = ticker.news()  # Call the method to get the news data
            
            print(f"Raw news data for {symbol}: {news}")  # Print raw news to inspect the structure

            # Check if news contains an error message
            if isinstance(news, list) and len(news) == 1 and news[0] == 'error':
                print(f"Error fetching news for {symbol}: News data is unavailable.")
                continue

            if isinstance(news, list):
                print(f"Fetched {len(news)} articles for {symbol}.")
                for i, article in enumerate(news, 1):
                    title = article.get('title', 'No title available')
                    link = article.get('link', 'No link available')
                    source = article.get('source', 'No source information')
                    date = article.get('pubDate', 'No publication date')
                    summary = article.get('summary', 'No summary available')

                    print(f"Article {i}:")
                    print(f"Title: {title}")
                    print(f"Link: {link}")
                    print(f"Source: {source}")
                    print(f"Date Published: {date}")
                    print(f"Summary: {summary}\n")
            else:
                print(f"The 'news' attribute for {symbol} is not in the expected list format.")
        
        except Exception as e:
            print(f"Error fetching news for {symbol}: {e}")
            continue

# Fetching news for gold-related symbols
fetch_gold_news()
