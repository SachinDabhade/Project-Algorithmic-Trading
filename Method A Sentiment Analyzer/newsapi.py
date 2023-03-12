import requests
import pandas as pd

class NewsApiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://newsapi.org/v2/everything?q=Indian%20market&apiKey={}".format(api_key)
        self.data = None
        
    def get_news(self):
        response = requests.get(self.url)
        data = response.json()
        news = data['articles']
        return news
    
    def store_data(self):
        news = self.get_news()
        df = pd.DataFrame(news)
        self.data = df.drop(columns=['source', 'author', 'url', 'urlToImage', 'publishedAt'])
        self.data.to_csv('NewsAPIClient.csv', index=False)
        return self.data