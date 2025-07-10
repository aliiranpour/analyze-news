import requests
from typing import TYPE_CHECKING
from utils.logger import get_logger
import os 

if TYPE_CHECKING:
    from models.news_types import NewsState

logger = get_logger(__name__)

def fetch_symbols(state: 'NewsState') -> 'NewsState':
    """
    دریافت لیست نمادهای معتبر از API بورس و ذخیره در state.

    - اطلاعات از SYMBOLS_URL خوانده می‌شود.
    - فیلدهای l18 (نماد به حروف فارسی) به‌عنوان نماد معتبر نگهداری می‌شوند.

    Args:
        state (NewsState): وضعیت فعلی.

    Returns:
        NewsState: وضعیت به‌روزشده شامل لیست کامل نمادها و مجموعه‌ای از نمادهای معتبر.
    """

    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 10))
    SYMBOLS_URL = os.getenv(
    "SYMBOLS_URL",
    "https://BrsApi.ir/Api/Tsetmc/AllSymbols.php?key=FreemX8CmT1EAXW20tZ9eXBJOHSzLwvJ"
    )

    logger.info("Fetching all symbols from %s", SYMBOLS_URL)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36 OPR/106.0.0.0"
        ),
        "Accept": "application/json, text/plain, */*"
    }

    try:
        resp = requests.get(SYMBOLS_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        state['symbols'] = data
        state['valid_symbol_names'] = set(
            item['l18'] for item in data if 'l18' in item
        )
        logger.info("Loaded %d valid symbols", len(state['valid_symbol_names']))
    except Exception as e:
        logger.error("Error fetching symbols: %s", e)
        state['symbols'] = []
        state['valid_symbol_names'] = set()

    return state
