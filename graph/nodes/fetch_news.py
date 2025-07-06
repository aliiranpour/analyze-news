from bs4 import BeautifulSoup
from models.news_types import Article, NewsState
import requests
from typing import List
from utils.logger import get_logger
import hashlib
import os


def fetch_news(state: NewsState) -> NewsState:
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
    logger = get_logger(__name__)
    logger.info("Fetching news articles")
    articles: List[Article] = []
    for link in state.get('links', []):
        try:
            resp = requests.get(link, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            div = soup.find('div', class_='newsMainBody') or soup.find('article')
            if not div:
                logger.warning("No content found for %s", link)
                continue
            text = div.get_text("\n", True)
            h = hashlib.sha256(text.encode()).hexdigest()
            articles.append({'link': link, 'content': text, 'hash': h})
        except Exception as e:
            logger.error("Error fetching %s: %s", link, e)
    state['articles'] = articles
    logger.info("Fetched %d articles", len(articles))
    return state
