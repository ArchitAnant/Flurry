import json
import csv
import requests

class TrendsAnalyzer:
    def __init__(self):
        self.api_key = "api_key"
        self.input_files = {
            "Technology": "data/processed/technology.csv",
            "Global_Political": "data/processed/global_politics.csv",
            "India_Political": "data/processed/political_news.csv",
            "Sports": "data/processed/sports.csv",
            "Finance": "data/processed/finance.csv"
        }

    def analyze_trends(self, category):
        """Analyze trends for a specific category"""
        if category not in self.input_files:
            raise ValueError(f"Invalid category: {category}")
        
        headlines = self._extract_headlines(self.input_files[category])
        results = []
        
        for headline in headlines:
            trend_data = self._get_trend_data(headline)
            if trend_data:
                results.append({
                    "headline": headline,
                    "last_three_points": trend_data
                })
        
        output_file = f"data/processed/{category.lower()}_trends.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"Saved trend data for {len(results)} headlines to {output_file}")
        return output_file

    def _extract_headlines(self, filename):
        """Extract headlines from CSV file"""
        headlines = []
        with open(filename, mode='r', encoding='utf-8') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                headlines.append(row['Headline'])
        return headlines

    def _get_trend_data(self, query):
        """Get trend data from SerpAPI"""
        params = {
            "engine": "google_trends",
            "q": query,
            "csv": "true",
            "data_type": "TIMESERIES",
            "api_key": self.api_key
        }
        
        try:
            response = requests.get("https://serpapi.com/search.json", params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'csv' in data:
                csv_lines = [line for line in data['csv'] if line.strip() and line[0].isdigit()]
                return csv_lines[-3:] if len(csv_lines) >= 3 else csv_lines
        except Exception as e:
            print(f"Error fetching trend data for '{query}': {str(e)}")
        return None

    def filter_trends(self, input_file):
        """Filter trends based on specific conditions"""
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        filtered_results = []
        
        for entry in data:
            points = entry["last_three_points"]
            if len(points) < 3:
                continue
            
            try:
                day1 = int(points[0].split(',')[1])
                day2 = int(points[1].split(',')[1])
                day3 = int(points[2].split(',')[1])
            except (IndexError, ValueError):
                continue
            
            if (day1 < day2 or day1 < day3) and (day3 >= 55 or day2 >= 55):
                filtered_results.append(entry)
        
        output_file = input_file.replace('.json', '_filtered.json')
        with open(output_file, 'w') as f:
            json.dump(filtered_results, f, indent=2)
        
        print(f"\nHeadlines with increasing trends (day2 or day3 ≥55):")
        for result in filtered_results:
            print(f"\n{result['headline']}:")
            for point in result["last_three_points"]:
                print(f"  {point}")
        
        print(f"\nFiltered results saved to {output_file}")
        return output_file