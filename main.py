import newsapi
import sentiment_analyzer
import NLTK_Analyzer

if __name__ == "__main__":

    # Loading Data From News API
    api_key = "726dad670180483fa1e7ba4381db5f69"
    client = newsapi.NewsApiClient(api_key)
    df = client.store_data()

    # Analyze Market Sentiment using IndianMarketSentimentAnalyzer
    analyzer = sentiment_analyzer.IndianMarketSentimentAnalyzer(df)
    analyzer.add_data()

    # Analyze Market Sentiment using NLTK Sentiment Analyzer
    analyzer = NLTK_Analyzer.NLTK_Analyzer(df)
    analyzer.Add_data()


