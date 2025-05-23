import requests
import re
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random as rn
import logging
import random as rn

load_dotenv()
keys = [os.environ["NEWS_API_KEY"],os.environ["NEWS_API_KEY1"]]
def get_news_links(topic):
    try:
        key = rn.choice(keys)
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=popularity&apiKey={key}"
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        response = requests.get(url,headers=headers)  
        response.raise_for_status()
        data = response.json()
        return [item['url'] for item in data.get('articles', [])[:min(4,len(data['articles']))] if 'url' in item]
    except Exception as e:
        print(f"Error fetching news links: {e}")
        return []
keys = [os.environ['GEMINI_API_KEY'],os.environ['GEMINI_API_KEY1']]
genai.configure(api_key=keys[rn.randint(0,1)])
model = genai.GenerativeModel("gemini-2.0-flash")

def scrape_articles_and_save(urls, topic):
    text = []
    for url in urls:
        try:
            res = requests.get(url, timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            res.raise_for_status()
            soup = BeautifulSoup(res.text, 'html.parser')
            paragraphs = soup.find_all('p')
            content = " ".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())
            if content:
                text.append(content)
        except Exception as e:
            logging.info(f"Error scraping {url}: {e}")
    
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
            logging.info(f"Error generating summary: {e}")
    
    return summary

def generate_script(topic):
    urls = get_news_links(topic)
    combined_text = scrape_articles_and_save(urls, topic)
    system_prompt = """You are a content creator scriptwriter creating in-depth catchy scripts addressing to a audience. 
            Structure your output with these exact section headers generate two scripts long script and short script.
            long script is about 400-500 words and short script is about 100-150 words.
            and also generate a list of 4 related hook words to the main topic.
            Use the following format and don't put the markers in the script: 

            **LONG SCRIPT**
            [ONE LINER]
            [8 words, AP Style]
            
            [SUMMARY LEAD (50 words, hard news hook)]

                [MAIN SCRIPT]
                    [Put News Facts]

                    [Background Context]

                    [About the event(if any)]
                    

            [CLOSING SUMMARY]
                [20 words]
                
            **SHORT SCRIPT**
            [ONE LINER]
            [SHORT OVERVIEW]
            [SMALL TOPIC SUMMARY]
            [CLOSE]

            **END OF SCRIPT**
            [4 related hook words]
            [4 words, separated by new lines]
            [Do not put any extra text or explanation]
            """

    try:
        
        prompt = f"{system_prompt}\n\nCreate a news package about: {topic}\n\nInformation to use:\n{combined_text}"
        response = model.generate_content(prompt)
        cleaned_content = response.text.strip()

        
        def extract_section(pattern, content):
            match = re.search(pattern, content, re.DOTALL)
            return match.group(1).strip() if match else ""

        long_script = extract_section(r"\*\*LONG SCRIPT\*\*\s*(.*?)(?=\n\s*\*\*SHORT SCRIPT|\Z)", cleaned_content)
        short_script = extract_section(r"\*\*SHORT SCRIPT\*\*\s*(.*?)(?=\n\s*\*\*END OF SCRIPT|\Z)", cleaned_content)
        
        related_topics_prompt = f"Generate a list of 4 related topics to '{topic}' with each topic being 1-3 words, separated by new lines"
        related_response = model.generate_content(related_topics_prompt)
        hook_topics = [t.strip() for t in related_response.text.strip().split("\n") if t.strip()]
        return {
            "short_script": short_script,#f"{headline}\n\n{summary_lead}".strip(),
            "long_script": long_script,#f"{main_script}\n\n{closing_summary}".strip(),
            "hook_topics": hook_topics
        }

    except Exception as e:
        logging.info(f"Error generating news package: {e}")
        return {
            "short_script": "",
            "long_script": "",
            "hook_topics": []
        }
