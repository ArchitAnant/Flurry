from groq import Groq
from dotenv import load_dotenv
import os
import random as rn
import json

load_dotenv()

api_key=[os.environ["GROQ_API_KEY"],os.environ["GROQ_API_KEY1"]]

def evaluate_image(image_url):
    """
    This function evaluates an image using the Groq API.
    It identifies famous people, places, and text in the image,
    and returns a JSON object with these details.
    """
    client = Groq(api_key=rn.choice(api_key))
    
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "analyse this image and identify famous people, famous/Well known places only, text in the image. return me a json with the list of these items and use these informations to make a small phrase 4 to 5 words to describe this image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{image_url}"
                        }
                    }
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        response_format={"type": "json_object"},
        stop=None,
    )

    resp = completion.choices[0].message.content
    parsed_json = json.loads(resp)
    return parsed_json


