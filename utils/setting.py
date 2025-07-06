import os
from dotenv import load_dotenv

load_dotenv()

BASE_DELAY = float(os.getenv("BASE_DELAY", 1.0))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
CACHE_FILE = os.getenv("CACHE_FILE", "news_summary_cache.json")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 10))
