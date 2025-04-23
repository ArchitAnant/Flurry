import requests
import datetime as dt
from dotenv import load_dotenv
import os
import time
import random as rn

load_dotenv()
keys = [os.environ["GNEWS_API_KEY"],os.environ["GNEWS_API_KEY1"]]
def get_headlines(date,category="world"):
    news = []
    apikey = keys[rn.randint(0,1)] 
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&from={date}T00:00:00Z&to={date}T23:59:59Z&max=10&apikey={apikey}"
    headers = {
        "User-Agent": "Mozilla/5.0",
    }
    response = requests.get(url, timeout=15,headers=headers)  

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
    days = []
    for i in range(1, 4):
        time.sleep(2)
        date = dt.datetime.now() - dt.timedelta(days=i)
        date = date.strftime("%Y-%m-%d")
        days.append(
            {date: get_headlines(date,cat)}
        )

    import json
    with open(f"/tmp/{cat}_news.json", "w") as f:
        json.dump(days, f, indent=4)



