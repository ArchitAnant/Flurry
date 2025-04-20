import json
import requests
import time

class NewsFetcher:
    def __init__(self):
        self.accounts = {
            "Technology": {"id": "10876852", "filename": "data/raw/technology_news.txt"},
            "India_Political": {"id": "355989081", "filename": "data/raw/india_political_news.txt"},
            "Global_Political": {"id": "742143", "filename": "data/raw/global_political_news.txt"},
            "Sports": {"id": "1144538493441343488", "filename": "data/raw/sports_news.txt"},
            "Finance": {"id": "39743812", "filename": "data/raw/stock_market_news.txt"}
        }
        self.headers = {
            "x-rapidapi-key": "API_KEY",
            "x-rapidapi-host": "twitter241.p.rapidapi.com"
        }

    def fetch_tweets(self, category):
        """Fetch tweets for a specific category"""
        if category not in self.accounts:
            raise ValueError(f"Invalid category: {category}")
        
        account_info = self.accounts[category]
        url = "https://twitter241.p.rapidapi.com/user-tweets"
        querystring = {"user": account_info["id"], "count": "200"}
        
        try:
            response = requests.get(url, headers=self.headers, params=querystring)
            response.raise_for_status()
            return self._extract_tweets(response.json())
        except Exception as e:
            print(f"Error fetching tweets for {category}: {str(e)}")
            return []

    def _extract_tweets(self, response_data):
        """Extract full text from tweets in the API response"""
        full_texts = []
        for entry in response_data.get("result", {}).get("timeline", {}).get("instructions", []):
            if entry.get("type") == "TimelineAddEntries":
                for tweet_entry in entry.get("entries", []):
                    if tweet_entry.get("content", {}).get("entryType") == "TimelineTimelineItem":
                        tweet_content = tweet_entry.get("content", {}).get("itemContent", {}).get("tweet_results", {}).get("result", {})
                        legacy_tweet = tweet_content.get("legacy", {})
                        full_text = legacy_tweet.get("full_text", "")
                        if full_text:
                            full_texts.append(full_text)
        return full_texts

    def save_tweets(self, tweets, category):
        """Save tweets to a text file"""
        if category not in self.accounts:
            raise ValueError(f"Invalid category: {category}")
        
        with open(self.accounts[category]["filename"], "a", encoding="utf-8") as file:
            for text in tweets:
                file.write(text + "\n\n")
        print(f"Saved {len(tweets)} tweets to {self.accounts[category]['filename']}")