import requests
import os
import random as rn
import datetime as dt
from dotenv import load_dotenv
import os

load_dotenv()

def get_trend_values(topic):
    startDate = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%d")
    endDate = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%d")
    api_key = [os.environ['SEPAPI_API_KEY1'],os.environ['SEPAPI_API_KEY2']]
    params = {
        "engine": "google_trends",
        "q": topic,
        "data_type": "TIMESERIES",
        "date": f"2025-04-{startDate}T10 2025-04-{endDate}T22",
        "api_key": api_key[rn.randint(0,1)]
    }
    value_list = [topic,0]
            
    try:
        response = requests.get("https://serpapi.com/search.json", params=params)
        response.raise_for_status()
        data = response.json()
        timeline_data = data['interest_over_time']['timeline_data']
        count = 0
        for i in range(len(timeline_data)):
            value = timeline_data[i]['values'][0]['extracted_value']
            if value > 45:
                count+=1

        value_list = [topic,count]
    except Exception as e:
        print("Error:",e)
    return value_list

