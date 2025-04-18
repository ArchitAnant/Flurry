# pip install python-dotenv
from dotenv import load_dotenv
import os


load_dotenv()
# use a .env file to save your API keys and use like
# api_key = os.environ["GROQ_API_KEY"]

def generate_script(topic : str) -> dict:
    """
    TODO
    parameter:
    topics (str) : Catch word -> 2-3 word phrase which is trending.

    Find the related trending topics using Serpapi.
    For Each trending topic and main topic ->  
    Use Gnews api or any other way you want to fetch latest news (last 2-3 days) on that topic. Extract news articles.
    Use these artcles and catch words (trending words) to generate -> short script (30-90 seconds long) and long script(5-12 minutes long)

    return:
    A dict as
    {
        "short_script" : str,
        "long_script" : str
    }
    """
    pass