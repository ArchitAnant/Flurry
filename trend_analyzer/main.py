from modules.news_fetcher import NewsFetcher
from modules.news_processor import NewsProcessor
from modules.trends_analyzer import TrendsAnalyzer

class TrendAnalyzerApp:
    def __init__(self):
        self.fetcher = NewsFetcher()
        self.processor = NewsProcessor()
        self.analyzer = TrendsAnalyzer()
        self.categories = {
            "1": "Technology",
            "2": "Global_Political",
            "3": "India_Political",
            "4": "Sports",
            "5": "Finance"
        }

    def run(self):
        while True:
            self._display_menu()
            choice = input("Enter your choice (1-6): ")
            
            if choice == "6":
                print("Exiting the application. Goodbye!")
                break
            
            if choice in self.categories:
                category = self.categories[choice]
                self._process_category(category)
            else:
                print("Invalid choice. Please try again.\n")

    def _display_menu(self):
        print("\n===== Trend Analyzer Menu =====")
        print("1. Technology Trends")
        print("2. Global Politics Trends")
        print("3. India Politics Trends")
        print("4. Sports Trends")
        print("5. Finance Trends")
        print("6. Exit")

    def _process_category(self, category):
        print(f"\nProcessing {category.replace('_', ' ')}...")
        
        # Step 1: Fetch news
        print("\nFetching latest news...")
        tweets = self.fetcher.fetch_tweets(category)
        if tweets:
            self.fetcher.save_tweets(tweets, category)
            
            # Step 2: Process news
            print("\nProcessing news with Gemini AI...")
            if self.processor.process_news(category):
                
                # Step 3: Analyze trends
                print("\nAnalyzing Google Trends data...")
                trends_file = self.analyzer.analyze_trends(category)
                
                # Step 4: Filter trends
                print("\nFiltering significant trends...")
                self.analyzer.filter_trends(trends_file)
        else:
            print(f"Failed to fetch news for {category}")

if __name__ == "__main__":
    app = TrendAnalyzerApp()
    app.run()