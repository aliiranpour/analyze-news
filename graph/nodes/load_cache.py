import os
import json
from typing import TYPE_CHECKING

from utils.setting import CACHE_FILE
from utils.logger import get_logger

if TYPE_CHECKING:
    from models.news_types import NewsState  

    
logger = get_logger(__name__)

def load_cache(state: 'NewsState') -> 'NewsState':
    """
    بارگذاری کش از فایل مشخص‌شده در تنظیمات و ذخیره در state.
    اگر فایل موجود نباشد یا خراب باشد، کش خالی مقداردهی می‌شود.
    """
    logger.info("Loading cache from %s", CACHE_FILE)
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                state['cache'] = json.load(f)
        else:
            state['cache'] = {}
    except (json.JSONDecodeError, IOError) as e:
        logger.error("Failed to load cache: %s", e)
        state['cache'] = {}

    return state
