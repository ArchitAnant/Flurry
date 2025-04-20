import csv
import re
from google.generativeai import configure, GenerativeModel

class NewsProcessor:
    def __init__(self):
        configure(api_key="api_key")
        self.model = GenerativeModel('gemini-2.0-flash')
        self.output_files = {
            "Technology": "data/processed/technology.csv",
            "Global_Political": "data/processed/global_politics.csv",
            "India_Political": "data/processed/political_news.csv",
            "Sports": "data/processed/sports.csv",
            "Finance": "data/processed/finance.csv"
        }

    def clean_text(self, text):
        """Clean tweet text by removing unwanted elements"""
        text = re.sub(r'http\S+|@\S+|RT\s+|#WATCH\s*|\|.*?:|Read @ANI Story.*', '', text)
        text = re.sub(r'\.\.\..*', '', text)
        return text.strip()

    def read_news_from_file(self, filename):
        """Read and clean news items from file"""
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        return [self.clean_text(item) for item in content.split('\n\n') if self.clean_text(item)]

    def process_news(self, category):
        """Process news for a specific category"""
        if category not in self.output_files:
            raise ValueError(f"Invalid category: {category}")
        
        input_file = f"data/raw/{category.lower()}_news.txt"
        news_items = self.read_news_from_file(input_file)
        
        prompt = self._get_prompt_template(category)
        processed_output = self._send_to_gemini(news_items, prompt)
        
        if processed_output:
            self._save_to_csv(processed_output, self.output_files[category])
            return True
        return False

    def _get_prompt_template(self, category):
        """Get appropriate prompt template with examples for each category"""
        templates = {
            "Technology": """
            Process these Technology news items and:
            1. Remove any duplicate/similar news (keep only one version)
            2. For each unique news item:
               - Create a maximum 3-word headline focusing on key tech entities/innovations
               - Generate a concise 20-word summary highlighting technical aspects
            3. Return in CSV format with columns: Headline,Summary

            Example:
            Input: "Apple unveils new M3 chip with 30% faster performance and AI capabilities at WWDC event"
            Output: "Apple M3 chip , New processor boasts 30% speed boost and enhanced AI features at WWDC conference."

            News items:
            """,
            
            "Global_Political": """
            Process these Global Political news items and:
            1. Remove any duplicate/similar news (keep only one version)
            2. For each unique news item:
               - Create a maximum 2-word headline focusing on countries/leaders/key events
               - Generate a concise 20-word summary of the geopolitical situation
            3. Return in CSV format with columns: Headline,Summary

            Example:
            Input: "UN Security Council emergency meeting called as tensions escalate between Russia and Ukraine over border clashes"
            Output: "UN Russia-Ukraine , Emergency Security Council meeting convened amid escalating border tensions and diplomatic standoff."

            News items:
            """,
            
            "India_Political": """
            Process these Indian Political news items and:
            1. Remove any duplicate/similar news (keep only one version)
            2. For each unique news item:
               - Create a maximum 2-word headline focusing on key entities for Google Trends
               - Generate a concise 20-word summary of the political development
            3. Return in CSV format with columns: Headline,Summary

            Example:
            Input: "Delhi High Court issues notice to AAP government on plea challenging liquor policy amendments"
            Output: "Liquor policy, Delhi HC issues notice to AAP govt on plea challenging recent amendments to excise rules."

            News items:
            """,
            
            "Sports": """
            Process these Sports news items and:
            1. Remove any duplicate/similar news (keep only one version)
            2. For each unique news item:
               - Create a maximum 2-word headline focusing on teams/players/key moments
               - Generate a concise 20-word summary of the sporting event
            3. Return in CSV format with columns: Headline,Summary

            Example:
            Input: "India defeats Australia by 5 wickets in T20 World Cup semifinal with Kohli scoring 82*"
            Output: "India Australia, Kohli's 82* guides India to T20 WC final with 5-wicket victory over Australia."

            News items:
            """,
            
            "Finance": """
            Process these Financial news items and:
            1. Remove any duplicate/similar news (keep only one version)
            2. For each unique news item:
               - Create a maximum 2-word headline focusing on markets/companies/economic indicators
               - Generate a concise 20-word summary of the financial development
            3. Return in CSV format with columns: Headline,Summary

            Example:
            Input: "Sensex crashes 800 points as RBI hikes interest rates by 50 basis points to combat inflation"
            Output: "Markets RBI, Sensex plunges 800 points after surprise 50bps rate increase to curb rising inflation."

            News items:
            """
        }
        return templates.get(category, "Process these news items:")

    def _send_to_gemini(self, news_items, prompt):
        """Send news to Gemini for processing"""
        full_prompt = prompt + "\n\n".join([f"{i+1}. {item}" for i, item in enumerate(news_items)])
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Gemini processing error: {e}")
            return None

    def _save_to_csv(self, gemini_output, filename):
        """Save processed news to CSV file"""
        csv_lines = [line for line in gemini_output.split('\n') if ',' in line]
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Headline', 'Summary'])
            for line in csv_lines:
                parts = line.split(',', 1)
                if len(parts) == 2:
                    writer.writerow([parts[0].strip(), parts[1].strip()])
        print(f"Saved {len(csv_lines)} items to {filename}")