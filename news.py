import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

class StockRecommender:
    def __init__(self, url):
        self.url = url
        self.ticker_news = {}
        self.vectorizer = TfidfVectorizer()
    
    def get_text(self):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.content, "html.parser")
        self.text = " ".join([p.text for p in soup.find_all("p")])
    
    def extract_ticker_news(self):
        # Extract ticker and news information from the text and store in a dictionary
        lines = self.text.split("\n")
        for line in lines:
            if "stock" in line.lower():
                ticker = line.split(" ")[0].strip()
                news = " ".join(line.split(" ")[1:]).strip()
                self.ticker_news[ticker] = news
    
    def build_similarity_matrix(self):
        # Create a tf-idf matrix from the ticker news
        tfidf_matrix = self.vectorizer.fit_transform(self.ticker_news.values())
        self.similarity_matrix = cosine_similarity(tfidf_matrix)
    
    def recommend_stocks(self, target_ticker):
        # Get the index of the target ticker in the similarity matrix
        target_index = list(self.ticker_news.keys()).index(target_ticker)
        
        # Get the similarity scores of the target ticker with all other tickers
        similarity_scores = self.similarity_matrix[target_index]
        
        # Sort the similarity scores in descending order and get the indices of the top 5 most similar tickers
        top_indices = np.argsort(similarity_scores)[::-1][:5]
        
        # Get the top 5 most similar tickers based on the indices
        top_tickers = [list(self.ticker_news.keys())[i] for i in top_indices]
        
        return top_tickers

# Use the StockRecommender class to recommend stocks based on market news
url = "https://www.example.com/market-news"
recommender = StockRecommender(url)
recommender.get_text()
recommender.extract_ticker_news()
recommender.build_similarity_matrix()
target_ticker = "AAPL"
recommended_stocks = recommender.recommend_stocks(target_ticker)
print(f"Recommended stocks for {target_ticker}: {recommended_stocks}")
