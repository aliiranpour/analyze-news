import json
from typing import TYPE_CHECKING
from utils.setting import CACHE_FILE
from utils.logger import get_logger

if TYPE_CHECKING:
    from models.news_types import NewsState  # فقط برای type hint در زمان توسعه

logger = get_logger(__name__)

def save_cache(state: 'NewsState') -> 'NewsState':
    """
    ذخیره کش خلاصه‌ها در فایل مشخص‌شده با نام CACHE_FILE.
    """
    logger.info("Saving cache to %s", CACHE_FILE)
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(state.get('cache', {}), f, ensure_ascii=False, indent=2)
    except IOError as e:
        logger.error("Failed to save cache: %s", e)
    return state
