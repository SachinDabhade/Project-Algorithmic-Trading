import nltk
import requests
from bs4 import BeautifulSoup

# Get news articles about Indian market from a website
url = "https://www.example.com/indian-market-news"
html = requests.get(url)
soup = BeautifulSoup(html.content, "html.parser")
text = " ".join([p.text for p in soup.find_all("p")])

# Tokenize the text and remove stopwords
tokens = nltk.word_tokenize(text)
stopwords = nltk.corpus.stopwords.words("english")
tokens = [word for word in tokens if word.lower() not in stopwords]

# Perform sentiment analysis using nltk's SentimentIntensityAnalyzer
nltk.download("vader_lexicon")
sentiment_analyzer = nltk.SentimentIntensityAnalyzer()
sentiment = sentiment_analyzer.polarity_scores(" ".join(tokens))["compound"]

# Interpret the sentiment score
if sentiment >= 0.05:
    print("Positive sentiment")
elif sentiment <= -0.05:
    print("Negative sentiment")
else:
    print("Neutral sentiment")
