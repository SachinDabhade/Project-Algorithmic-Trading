import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import create_engine
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class StockRecommender:
    def __init__(self, url):
        self.url = url
        self.data = None
        self.engine = create_engine("sqlite:///stock_recommender.db")
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.cosine_sim = None

    def get_data(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text, 'html.parser')
        headlines = [header.get_text().strip() for header in soup.find_all("h3")]
        self.data = pd.DataFrame(headlines, columns=["Headlines"])

    def store_data(self):
        self.data.to_sql("news_data", self.engine, if_exists="replace")

    def recommend_stocks(self):
        tfidf_matrix = self.tfidf.fit_transform(self.data['Headlines'])
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        indices = pd.Series(self.data.index, index=self.data['Headlines'])
        idx = np.random.choice(self.data.index)
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        stock_indices = [i[0] for i in sim_scores]
        return self.data['Headlines'].iloc[stock_indices]

if __name__ == "__main__":
    url = "https://www.marketnews.com/top-news"
    recommender = StockRecommender(url)
    recommender.get_data()
    recommender.store_data()
    print(recommender.recommend_stocks())
