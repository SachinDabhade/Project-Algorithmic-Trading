from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import sqlite3

class IndianMarketSentimentAnalyzer:
    def __init__(self, data):
        self.data = data
        self.text = None
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self.conn = sqlite3.connect("Indian_Market_Sentiment.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment (
                sentiment text,
                probability text,
                text text
            )
        """)
    
    def analyze_sentiment(self):
        probability = self.sentiment_analyzer.polarity_scores(self.text)["compound"]
        return probability
    
    def interpret_sentiment(self):
        probability = self.analyze_sentiment()
        if probability > 0.05:
            return "Positive", probability
        elif probability < -0.05:
            return "Negative", probability
        else:
            return "Neutral", probability
    
    def add_data(self):
        for self.text in self.data['description']:
            sentiment, probability = self.interpret_sentiment()
            self.cursor.execute("""
                INSERT INTO sentiment (sentiment, probability, text)
                VALUES (?, ?, ?)
            """, (sentiment, probability, self.text))
            self.conn.commit()
            print(sentiment, probability, self.text)
        self.conn.close()