from google import genai
from google.genai import types
import json
import re
from dotenv import load_dotenv
import os
import random as rn

load_dotenv()


def parse_json(file_path):
    news = []
    with open(file_path, "r") as f:
        data = json.load(f)
        for day in data:
            for date, articles in day.items():
                for article in articles:
                    news.append(str(article))

    return "\n".join(news)

def generate(file_path):
    keys = [os.environ['GEMINI_API_KEY'],os.environ['GEMINI_API_KEY1']]
    news_data = parse_json(file_path)
    client = genai.Client(
        api_key=keys[rn.randint(0, 1)],
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"""{news_data}
parse this data and find 10 of the most trending phrase topics and tell me in 2-3 words return strict json format as list of topics"""),
            ],
        ),
    ]
    tools = [
        types.Tool(google_search=types.GoogleSearch())
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.9,
        top_p=0.7,
        tools=tools,
        response_mime_type="text/plain",
    )
    resp = []
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        resp.append(chunk.text)
    
    raw_text = resp[0].strip()
    cleaned_text = re.sub(r"^```json|```$", "", raw_text).strip()

    json_data = json.loads(cleaned_text)
    topics = []

    for i in range(len(json_data)):
        topics.append(json_data[i])
    
    return topics


