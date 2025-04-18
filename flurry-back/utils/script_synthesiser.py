from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timedelta
import time
from serpapi import GoogleSearch
from groq import Groq

load_dotenv(dotenv_path=r"C:\Users\jitro\OneDrive\Desktop\Hackathon\Flurry\flurry-back\utils\.env.local")

def get_related_trending_topics(topic):
    serpapi_key = os.getenv("SERPAPI_API_KEY")

    params = {
        "engine": "google_trends",
        "q": topic,
        "data_type": "RELATED_TOPICS",
        "api_key": serpapi_key
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    trending_topics = []

    if "related_topics" in results and "rising" in results["related_topics"]:
        for item in results["related_topics"]["rising"]:
            if "topic" in item and "title" in item["topic"]:
                trending_topics.append(item["topic"]["title"])

    return trending_topics[:5]

def fetch_news_articles(topics):
    """
    Fetch recent news articles for the given topics using GNews API.
    
    Args:
        topics (list): List of topics to fetch news for
        
    Returns:
        list: List of news article content and metadata
    """
    gnews_api_key = os.environ["GNEWS_API_KEY"]
    articles = []
    
    # Calculate date for the last 3 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3)
    from_date = start_date.strftime("%Y-%m-%d")
    to_date = end_date.strftime("%Y-%m-%d")
    
    for topic in topics:
        try:
            # Format the URL with query parameters
            url = f"https://gnews.io/api/v4/search?q={topic}&lang=en&country=us&max=5&from={from_date}T00:00:00Z&to={to_date}T23:59:59Z&apikey={gnews_api_key}"
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                if "articles" in data:
                    for article in data["articles"]:
                        articles.append({
                            "title": article["title"],
                            "description": article["description"],
                            "content": article["content"],
                            "url": article["url"],
                            "source": article["source"]["name"],
                            "related_topic": topic
                        })
                
            # Add delay to avoid rate limiting
            time.sleep(1)
                
        except Exception as e:
            print(f"Error fetching news for topic '{topic}': {e}")
    
    return articles

def generate_scripts_with_llm(main_topic, articles):
    """
    Generate short and long scripts using an LLM based on the articles and trending topics.
    
    Args:
        main_topic (str): The main topic or catchword
        articles (list): List of news article content and metadata
        
    Returns:
        dict: Dictionary containing short and long scripts
    """
    # Create context from articles
    articles_context = ""
    for i, article in enumerate(articles[:10]):  # Limit to first 10 articles to avoid token issues
        articles_context += f"Article {i+1}:\n"
        articles_context += f"Title: {article['title']}\n"
        articles_context += f"Source: {article['source']}\n"
        articles_context += f"Description: {article['description']}\n"
        articles_context += f"Content: {article['content']}\n"
        articles_context += f"Related to topic: {article['related_topic']}\n\n"

    # Check if we have any articles to work with
    if not articles_context:
        return {
            "short_script": f"No recent news found about {main_topic}.",
            "long_script": f"We couldn't find any recent news articles about {main_topic} in the past few days."
        }
    
    # Initialize Groq client
    groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])
    
    # Prepare prompt for short script (30-90 seconds)
    short_script_prompt = f"""
You are a professional script writer for short-form video content. 
I need you to create a script about the trending topic: "{main_topic}".

Here are recent news articles related to this topic:
{articles_context}

Create a SHORT SCRIPT for a 30-90 second video that:
1. Covers the most newsworthy and exciting developments
2. Starts with a hook to grab attention
3. Includes 2-3 key points about the topic
4. Ends with a clear conclusion or call to action
5. Uses conversational language suitable for platforms like TikTok or Instagram Reels
6. Includes [VISUAL CUE] notes for visuals where appropriate

THE SCRIPT SHOULD BE 150-250 WORDS MAXIMUM.
"""

    # Prepare prompt for long script (5-12 minutes)
    long_script_prompt = f"""
You are a professional script writer for long-form video content.
I need you to create a script about the trending topic: "{main_topic}".

Here are recent news articles related to this topic:
{articles_context}

Create a LONG SCRIPT for a 5-12 minute video that:
1. Provides comprehensive coverage of the topic with depth and nuance
2. Has a clear structure: introduction, several main sections, and conclusion
3. Includes relevant background information when needed
4. Explores different perspectives on the topic
5. Cites specific information from the articles
6. Uses engaging, educational language suitable for platforms like YouTube
7. Includes [VISUAL CUE] notes for visuals or b-roll where appropriate
8. Includes timestamps for different sections

THE SCRIPT SHOULD BE 800-1500 WORDS.
"""

    try:
        # Generate short script
        short_response = groq_client.chat.completions.create(
            model="llama3-70b-8192",  # Or use mixtral-8x7b-32768 or any other available model
            messages=[
                {"role": "system", "content": "You are a helpful scriptwriter that creates engaging video scripts based on trending topics and news."},
                {"role": "user", "content": short_script_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        short_script = short_response.choices[0].message.content
        
        # Generate long script
        long_response = groq_client.chat.completions.create(
            model="llama3-70b-8192",  # Or use mixtral-8x7b-32768 or any other available model
            messages=[
                {"role": "system", "content": "You are a helpful scriptwriter that creates engaging video scripts based on trending topics and news."},
                {"role": "user", "content": long_script_prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        long_script = long_response.choices[0].message.content
        
        return {
            "short_script": short_script,
            "long_script": long_script
        }
        
    except Exception as e:
        print(f"Error generating scripts: {e}")
        return {
            "short_script": f"Error generating short script for {main_topic}: {str(e)}",
            "long_script": f"Error generating long script for {main_topic}: {str(e)}"
        }


def generate_script(topic: str) -> dict:
    """
    Generate short and long scripts for a trending topic.
    
    Parameters:
    topic (str): Catch word -> 2-3 word phrase which is trending.

    Returns:
    A dict as
    {
        "trending_topics": list
        "short_script": str,
        "long_script": str,
    }
    """
    # Step 1: Get related trending topics
    trending_topics = get_related_trending_topics(topic)
    print(f"Found trending topics: {trending_topics}")
    
    # Step 2: Fetch recent news articles
    articles = fetch_news_articles(trending_topics)
    print(f"Found {len(articles)} news articles")
    
    # Step 3: Generate scripts using an LLM
    scripts = generate_scripts_with_llm(topic, articles)
    
    return {
        "trending_topics": trending_topics,
        **scripts
    }

# Example usage
# if __name__ == "__main__":
#     topic = "AI"
#     scripts = generate_script(topic)
#     print(scripts)