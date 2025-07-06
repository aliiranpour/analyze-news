import os
import feedparser
import requests
import logging
from typing import TypedDict, List, Dict
from models.news_types import  NewsState
from utils.logger import get_logger


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = get_logger(__name__)

RSS_URL = os.getenv("RSS_URL", "https://www.eghtesadonline.com/rss")

def fetch_rss(state: NewsState) -> NewsState:
    logger.info("Fetching RSS feed: %s", RSS_URL)
    feed = feedparser.parse(RSS_URL)
    state['links'] = [entry.link for entry in feed.entries]
    logger.info("Found %d links", len(state['links']))
    return state