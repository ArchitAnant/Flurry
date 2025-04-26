import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
key = os.environ["NEWS_API_KEY"]
def get_headlines(category="general"):
    news = []
    url = f"https://newsapi.org/v2/top-headlines?category={category}&apiKey={key}"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.get(url, timeout=5,headers=headers)  
    response.raise_for_status()
    data = response.json()
    articles = data.get("articles", [])

    for article in articles:
        news.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "content": article.get("content"),
        })

    return news


def get_news(cat):
    with open(f"/tmp/{cat}_news.json", "w") as f:
        json.dump([{"articles": get_headlines(cat)}], f, indent=4)



