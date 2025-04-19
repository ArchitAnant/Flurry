import requests
from bs4 import BeautifulSoup
import os
import json
import re
from dotenv import load_dotenv
from serpapi import GoogleSearch
load_dotenv()  




def get_news_links(topic):
    params = {
        "engine": "google_news",
        "gl": "us",
        "hl": "en",
        "q": topic,
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }

    try:
        response = requests.get('https://serpapi.com/search', params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return [item['link'] for item in data.get('news_results', [])[:2] if 'link' in item]
    except Exception as e:
        print(f"Error fetching news links: {e}")
        return []

def scrape_articles_and_save(urls):
    text = []
    for url in urls:
        try:
            res = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = " ".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
            if content:
                text.append(content)
            else:
                print(f"No content found for {url}")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return text

def generate_news_package(topic):
    urls = get_news_links(topic)
    article_texts = scrape_articles_and_save(urls)
    combined_text = " ".join(article_texts)

    system_prompt = {
        "role": "system",
        "content": """You are a senior news scriptwriter creating in-depth 400-word news packages. Do not use first-person view and do not give any opinion.
                    Structure your output as follows:

                    1. HEADLINE (8 words, AP Style)
                    2. SUMMARY LEAD (50 words, hard news hook)
                    3. MAIN SCRIPT (300 words structured in sections):
                    a) Breaking News Facts
                    b) Background Context
                    c) Timeline of Events

                    4. CLOSING SUMMARY (20 words)
                    """
    }

    user_prompt = {
        "role": "user",
        "content": f"Create a professional news package about {topic} based on this information:\n\n{combined_text}"
    }

    payload = {
        "messages": [system_prompt, user_prompt],
        "model": "deepseek-r1-distill-llama-70b",
        "temperature": 0.7
    }

    groq_api_key = os.getenv("GROQ_API_KEY")
    headers = {
        "Authorization": f"Bearer {groq_api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            raw_content = response.json()["choices"][0]["message"]["content"]
            cleaned_content = re.sub(r"<think>.*?</think>", "", raw_content, flags=re.DOTALL).strip()

            
            summary_lead_match = re.search(r"2\. SUMMARY LEAD\s*\n(.*?)(?=\n3\.|$)", cleaned_content, re.DOTALL)
            summary_lead = summary_lead_match.group(1).strip() if summary_lead_match else ""

            long_script_parts = re.sub(r"2\. SUMMARY LEAD\s*\n.*?(?=\n3\.|$)", "", cleaned_content, flags=re.DOTALL).strip()

            # Basic hook_topics from topic (can be enhanced with NLP)
            hook_topics = [word.strip() for word in topic.split() if len(word) > 3]

            print("News package generated successfully.")
            return {
                "short_script": summary_lead,
                "long_script": long_script_parts,
                "hook_topics": hook_topics
            }
        else:
            print(f"Error generating news package: {response.status_code} - {response.text}")
            return {"short_script": "", "long_script": "", "hook_topics": []}
    except Exception as e:
        print(f"Error generating news package: {e}")
        return {"short_script": "", "long_script": "", "hook_topics": []}





 
        
