import time
from typing import Union
from langchain_core.runnables import Runnable
from utils.setting import BASE_DELAY, MAX_RETRIES
from utils.logger import get_logger

logger = get_logger(__name__)

def call_chain_with_backoff(chain: Union[Runnable, callable], inputs: dict):
    """
    اجرای LLM chain با backoff در صورت خطاهای موقتی (429, 504, ...).
    """
    delay = BASE_DELAY

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            if hasattr(chain, 'invoke'):
                return chain.invoke(inputs)
            else:
                return chain(inputs)
        except Exception as e:
            err = str(e)

            if any(code in err for code in ['429', 'Too Many Requests', '504', 'Gateway']):
                logger.warning(
                    "LLM call failed (%s), retry %d/%d after %.1f seconds",
                    e, attempt, MAX_RETRIES, delay
                )
                time.sleep(delay)
                delay *= 2
            else:
                logger.error("LLM call error: %s", e)
                raise

    raise RuntimeError(f"LLM call failed after {MAX_RETRIES} attempts")
