import json
import requests
import re
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
import google.generativeai as genai

def get_news_links(topic):
    params = {
        "engine": "google_news",
        "q": topic,
        "api_key": os.getenv("SERPAPI_API_KEY"),
    }

    try:
        response = requests.get('https://serpapi.com/search', params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return [item['link'] for item in data.get('news_results', [])[:4] if 'link' in item]
    except Exception as e:
        print(f"Error fetching news links: {e}")
        return []

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def scrape_articles_and_save(urls, topic):
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
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    
    if not text:
        return "No content available"

    summary = text[0]
    for article in text[1:]:
        prompt = f"""
                    You are an intelligent summarizer.

                    Below is the current summary of previous article(s):
                    {summary}

                    Here is a new article:
                    {article}

                    about the topic: {topic}

                    Compare the new article with the existing summary. Update the summary by incorporating any **new**, **important**, or **different** information from the new article. Avoid repeating things already mentioned.
                    Give a concise, updated news in 1000 words.
                """
        try:
            response = model.generate_content(prompt)
            summary = response.text.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
    
    return summary

def generate_news_package(topic):
    urls = get_news_links(topic)
    combined_text = scrape_articles_and_save(urls, topic)
    
    

    system_prompt = """You are a senior news scriptwriter creating in-depth 600-word news packages. 
            Structure your output with these exact section headers:

            **HEADLINE**
            [8 words, AP Style]
            
            SUMMARY LEAD (50 words, hard news hook)

                **MAIN SCRIPT**

                    **a) Breaking News Facts**
                    [content]

                    **b) Background Context**
                    [content]

                    **c) Timeline of Events**
                    [content]
                    

            **CLOSING SUMMARY**
                [20 words]"""

    try:
        
        prompt = f"{system_prompt}\n\nCreate a news package about: {topic}\n\nInformation to use:\n{combined_text}"
        response = model.generate_content(prompt)
        cleaned_content = response.text.strip()

        
        def extract_section(pattern, content):
            match = re.search(pattern, content, re.DOTALL)
            return match.group(1).strip() if match else ""

        headline = extract_section(r"\*\*HEADLINE\*\*\s*(.*?)(?=\n\s*\*\*SUMMARY|\Z)", cleaned_content)
        summary_lead = extract_section(r"\*\*SUMMARY LEAD\*\*\s*(.*?)(?=\n\s*\*\*MAIN|\Z)", cleaned_content)
        main_script = extract_section(r"\*\*MAIN SCRIPT\*\*\s*(.*?)(?=\n\s*\*\*CLOSING|\Z)", cleaned_content)
        closing_summary = extract_section(r"\*\*CLOSING SUMMARY\*\*\s*(.*?)(?=\n|\Z)", cleaned_content)

        
        related_topics_prompt = f"Generate a list of 4 related topics to '{topic}' with each topic being 1-3 words, separated by new lines"
        related_response = model.generate_content(related_topics_prompt)
        hook_topics = [t.strip() for t in related_response.text.strip().split("\n") if t.strip()]

        return {
            "short_script": f"{headline}\n\n{summary_lead}\n\n{closing_summary}".strip(),
            "long_script": main_script.strip(),
            "hook_topics": hook_topics
        }

    except Exception as e:
        print(f"Error generating news package: {e}")
        return {
            "short_script": "",
            "long_script": "",
            "hook_topics": []
        }

