from utils.fetch_news import get_news
from utils.raw_trends import generate
from dotenv import load_dotenv
from utils.trend_filters import get_trend_values
import json

load_dotenv()

cat_list = ["world", "business", "technology", "entertainment", "sports", "science"]
cat_topic_list = []
trends_map = []


def get_newses():
    for cat in cat_list:
        get_news(cat)

def get_topics():
    for cat in cat_list:
        topics = generate(f"./utils/raws/{cat}_news.json")
        cat_topic_list.append({cat : topics})

def get_trends():
    print("Collecting News...")
    get_newses()
    print("Collected News\nFetching Topics...")
    get_topics()
    print("Evaluating Topics...")
    for i in range(len(cat_list)):
        cat = cat_list[i]
        topics = cat_topic_list[i][cat]
        selected_topics = []
        for topic in topics:
            trend_count = get_trend_values(topic)
            if trend_count[1]>5:
                selected_topics.append(trend_count[0])
        trends_map.append({cat : selected_topics})
    print("Writing Values...")
    print(trends_map)
    with open(f"trends.json", "w") as f:
        json.dump(trends_map, f, indent=4)

    

