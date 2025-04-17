import json
import urllib.request
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

def get_headlines(date,category="world"):
    news = []
    apikey = os.environ["GNEWS_API_KEY"]
    
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&from=2025-04-{date}T00:00:00Z&to=2025-04-{date}T23:59:59Z&max=10&apikey={apikey}"

    with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
        articles = data["articles"]
        for i in range(len(articles)):
            curr_news = {}
            curr_news["title"] = articles[i]["title"]
            curr_news["description"] = articles[i]["description"]
            curr_news["content"] = articles[i]["content"]
            news.append(curr_news)

    return news


def get_news(cat):
    days = []
    for i in range(1, 4):
        date = dt.datetime.now() - dt.timedelta(days=i)
        date = date.strftime("%d")
        days.append(
            {date: get_headlines(date,cat)}
        )

    import json
    with open(f"./utils/raws/{cat}_news.json", "w") as f:
        json.dump(days, f, indent=4)

# available categories general, world, nation, business, technology, entertainment, sports, science and health.



