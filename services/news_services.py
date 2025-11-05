# services/news_service.py

import os
from services.contextCheckers import NameEntityRecognition,KeyWordExtractor
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()
news_api_key = os.getenv("NEWS_API_KEY")

newsapi = NewsApiClient(api_key=news_api_key)


def getTopic(text: str) -> str:
    ner_words =  NameEntityRecognition(text).nerPipeline_and_Check()
    keywords = KeyWordExtractor(text).keywordExtractor()
    keyword_strings = [kw[0] for kw in keywords]
    topic = " AND ".join(ner_words + keyword_strings) if ner_words or keywords else text
    return topic


def get_latest_news(text: str, limit: int = 5):
    """Fetch latest news articles on a given topic."""
    topic = getTopic(text=text)
    response = newsapi.get_everything(
        q=topic,
        language="en",
        sort_by="publishedAt",
        page_size=limit,
    )

    articles = response.get("articles", [])
    # Extract only title + description for summarization
    combined_text = "\n".join(
        f"- {article['title']}: {article.get('description', '')}"
        for article in articles
    )

    return combined_text or "No recent news found on this topic."
