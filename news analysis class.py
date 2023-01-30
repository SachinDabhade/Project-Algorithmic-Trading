import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3

class IndianMarketSentimentAnalyzer:
    def __init__(self, url):
        self.url = url
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.conn = sqlite3.connect("Indian_Market_Sentiment.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment (
                date text,
                sentiment text,
                text text
            )
        """)
    
    def get_text(self):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.content, "html.parser")
        self.text = " ".join([p.text for p in soup.find_all("p")])
    
    def analyze_sentiment(self):
        sentiment = self.sentiment_analyzer.polarity_scores(self.text)["compound"]
        return sentiment
    
    def interpret_sentiment(self):
        sentiment = self.analyze_sentiment()
        if sentiment > 0.05:
            return "Positive"
        elif sentiment < -0.05:
            return "Negative"
        else:
            return "Neutral"
    
    def add_data(self, date):
        sentiment = self.interpret_sentiment()
        self.cursor.execute("""
            INSERT INTO sentiment (date, sentiment, text)
            VALUES (?, ?, ?)
        """, (date, sentiment, self.text))
        self.conn.commit()
    
    def close_connection(self):
        self.conn.close()

# Use the IndianMarketSentimentAnalyzer class and store the results and text in a SQLite database
url = "https://www.example.com/indian-market-news"
sentiment_analyzer = IndianMarketSentimentAnalyzer(url)
sentiment_analyzer.get_text()
sentiment_analyzer.add_data("2023-01-30")
sentiment_analyzer.close_connection()
