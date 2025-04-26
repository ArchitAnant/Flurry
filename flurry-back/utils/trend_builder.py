from utils.fetch_news import get_news
from utils.raw_trends import generate
from dotenv import load_dotenv
import logging

load_dotenv()

cat_list = ["general", "business", "technology", "entertainment", "sports", "science"]
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
        trends_map.append({cat : topics})
    logging.info("Writing Values...")
    return trends_map

