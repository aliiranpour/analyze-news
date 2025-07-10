from typing import TYPE_CHECKING
from utils.logger import get_logger

if TYPE_CHECKING:
    from models.news_types import NewsState

logger = get_logger(__name__)

def print_cache(state: 'NewsState') -> 'NewsState':
    """
    نمایش محتوای کش همراه با اطلاعات کلیدی مثل لینک، هش، خلاصه، نمادها و کلمات کلیدی.
    """
    logger.info("Printing cache contents with keywords and symbols")
    cache = state.get('cache', {})
    print("\n=== Cached Summaries ===")
    
    for link, info in cache.items():
        print(f"Link: {link}")
        print(f"  Hash: {info.get('hash', '')}")
        print(f"  Summary: {info.get('summary', '')}")
        
        symbols = info.get('symbols', [])
        if symbols:
            print(f"  نمادهای موجود: {', '.join(symbols)}")
        
        filtered = state.get('filtered_symbols', [])
        if filtered:
            print(f"  نمادهای معتبر: {', '.join(filtered)}")

        keywords = info.get('keywords', [])
        if keywords:
            print(f"  Keywords: {', '.join(keywords)}")
        
        impact = info.get('impact', '')
        if impact:
            print(f"  Impact: {impact}")
        
        print() 
    
    print("=== End of Cache ===")
    return state
