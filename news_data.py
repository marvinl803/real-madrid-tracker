import requests
from bs4 import BeautifulSoup
from newspaper import Article, ArticleException
from requests.exceptions import HTTPError


class NewsApiClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"

    def get_articles(self, query):
        url = f"{self.base_url}/everything"
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "apiKey": self.api_key,
            "language": "en",
            "pageSize": 100,  # Limit the number of articles to retrieve
        }
        response = requests.get(url, params=params)
        data = response.json()
        articles = data.get("articles", [])
        processed_articles = []
        for article in articles:
            article_title = article.get("title", "")
            article_url = article.get("url", "")
            article_description = article.get("description", "")

            # Skip articles without title or URL
            if article_title and article_url:
                try:
                    article_data = {
                        "title": article_title,
                        "url": article_url,
                        "description": article_description
                    }
                    processed_articles.append(article_data)
                except (ArticleException, HTTPError) as e:
                    print(f"Error processing article: {str(e)}")
                    continue

        return processed_articles
