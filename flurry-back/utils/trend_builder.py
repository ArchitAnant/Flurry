from utils.fetch_news import get_news
from utils.raw_trends import generate
from dotenv import load_dotenv
from utils.trend_filters import get_trend_values
import json
import logging

load_dotenv()

cat_list = ["world", "business", "technology", "entertainment", "sports", "science"]
cat_topic_list = []
trends_map = []


def get_newses():
    for cat in cat_list:
        get_news(cat)

def get_topics():
    for cat in cat_list:
        topics = generate(f"/tmp/{cat}_news.json")
        cat_topic_list.append({cat : topics})

def get_trends():
    logging.info("Collecting News...")
    get_newses()
    logging.info("Collected News\nFetching Topics...")
    get_topics()
    logging.info("Evaluating Topics...")
    for i in range(len(cat_list)):
        cat = cat_list[i]
        topics = cat_topic_list[i][cat]
        selected_topics = []
        for topic in topics:
            trend_count = get_trend_values(topic)
            if trend_count[1]>5:
                selected_topics.append(trend_count[0])
        trends_map.append({cat : selected_topics})
    logging.info("Writing Values...")
    with open("trends.json", "w") as f:
        json.dump(trends_map, f, indent=4)

    

