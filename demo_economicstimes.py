import requests
from bs4 import BeautifulSoup
import pandas as pd

class NewsScraper:
    def __init__(self, url):
        self.url = url
        self.page = None
        self.soup = None

    def fetch_page(self):
        response = requests.get(self.url)
        self.page = response.text

    def parse_page(self):
        self.soup = BeautifulSoup(self.page, 'html.parser')

    def get_news(self):
        news_items = []
        news_list = self.soup.find('ul', {'class': 'list8'})
        for li in news_list.find_all('li'):
            headline = li.find('a').text
            news_items.append({'headline': headline})
        return news_items

scraper = NewsScraper('https://economictimes.indiatimes.com/news/india')
scraper.fetch_page()
scraper.parse_page()
news_items = scraper.get_news()

# Store the news in a Pandas DataFrame
df = pd.DataFrame(news_items)
print(df)
