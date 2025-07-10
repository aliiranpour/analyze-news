from typing import TYPE_CHECKING
from utils.logger import get_logger
from utils.parsers import parse_symbols  

if TYPE_CHECKING:
    from models.news_types import NewsState  

logger = get_logger(__name__)

def filter_symbols(state: 'NewsState') -> 'NewsState':
    """
    فیلتر کردن نمادهای استخراج‌شده از خلاصه خبر بر اساس نمادهای معتبر موجود.

    - اگر خلاصه‌ای در state موجود نباشد، state را بدون تغییر بازمی‌گرداند.
    - از تابع parse_symbols برای استخراج نمادها از متن استفاده می‌شود.
    - فقط نمادهایی که در لیست نمادهای معتبر هستند نگه داشته می‌شوند.

    Args:
        state (NewsState): وضعیت فعلی شامل لیست نمادها و خلاصه خبر.

    Returns:
        NewsState: وضعیت به‌روزشده با نمادهای فیلترشده در کلید filtered_symbols.
    """
    if not state.get("summary_output"):
        return state
    
    extracted_symbols = parse_symbols(state["summary_output"])
    
    valid_symbols = [item['l18'] for item in state.get('symbols', [])]

    filtered = [sym for sym in extracted_symbols if sym in valid_symbols]
    
    state["filtered_symbols"] = filtered
    logger.info("Filtered symbols: %s -> %s", extracted_symbols, filtered)
    return state
