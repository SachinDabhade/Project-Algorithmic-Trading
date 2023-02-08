import nltk
import sqlite3

# Downloading the veder lexicon
nltk.download("vader_lexicon")

class NLTK_Analyzer:
    def __init__(self, data):
        self.data = data
        self.text = None
        self.stopwords = nltk.corpus.stopwords.words("english")
        self.sentiment_analyzer = nltk.SentimentIntensityAnalyzer()
        self.conn = sqlite3.connect("NLTK_Analyzer.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sentiment (
                sentiment text,
                probability text,
                text text
            )
        """)

    def Tokenize(self):
        # Tokenize the text and remove stopwords
        tokens = nltk.word_tokenize(self.text)
        self.tokens = [word for word in tokens if word.lower() not in self.stopwords]

    def Analyzer(self):
        tokens = self.Tokenize()
        # Perform sentiment analysis using nltk's SentimentIntensityAnalyzer
        probability = self.sentiment_analyzer.polarity_scores(" ".join(tokens))["compound"]
        print(self.tokens, probability)
        return probability

    def Sentiment(self):
        probability = self.Analyzer()
        # Interpret the sentiment score
        if probability >= 0.05:
            return "Positive", probability
        elif probability <= -0.05:
            return "Negative", probability
        else:
            return "Neutral", probability

    def Add_data(self):
        for self.text in self.data:
            sentiment, probability = self.Sentiment()
            self.cursor.execute("""
                INSERT INTO sentiment (sentiment, probability, text)
                VALUES (?, ?, ?)
            """, (sentiment, probability, self.text))
            self.conn.commit()
            print(sentiment, probability, self.text)
        self.conn.close()