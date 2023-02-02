import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import newsapi

class StockRecommender:
    def __init__(self, data):
        self.data = data
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.cosine_sim = None

    def recommend_stocks(self):
        tfidf_matrix = self.tfidf.fit_transform(self.data['description'])
        self.cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        indices = pd.Series(self.data.index, index=self.data['description'])
        idx = np.random.choice(self.data.index)
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
        stock_indices = [i[0] for i in sim_scores]
        return self.data['title'].iloc[stock_indices]


if __name__ == "__main__":
    api_key = "726dad670180483fa1e7ba4381db5f69"
    client = newsapi.NewsApiClient(api_key)
    df = client.store_data()
    recommender = StockRecommender(df)
    print('stage1')
    print(recommender.data)
    print('stage2')
    print(recommender.recommend_stocks())
    print('stage3')
