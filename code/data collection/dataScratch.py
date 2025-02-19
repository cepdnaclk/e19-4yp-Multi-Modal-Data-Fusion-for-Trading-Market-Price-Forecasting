import requests
from bs4 import BeautifulSoup

def fetch_news():
    url = "https://www.investing.com/news/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract headlines and links
    news = []
    articles = soup.find_all("div", class_="articleItem")
    for article in articles:
        title = article.find("a", class_="title").text.strip()
        link = "https://www.investing.com" + article.find("a", class_="title")["href"]
        news.append({"title": title, "link": link})
    
    return news

news_list = fetch_news()
for item in news_list:
    print(item["title"], item["link"])
