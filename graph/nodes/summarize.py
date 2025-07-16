from langchain_core.prompts import ChatPromptTemplate
from models.news_types import NewsState
from utils.logger import get_logger
from utils.llm import get_llm
from utils.retry import call_chain_with_backoff 
from utils.setting import BATCH_SIZE 

llm = get_llm()
logger = get_logger(__name__)

def summarize_article(content: str) -> str:
    """تولید خلاصه‌ای دو جمله‌ای از خبر همراه با شرکت‌های بورسی"""

    prompt = ChatPromptTemplate.from_template(
        """
        شما یک تحلیلگر حرفه‌ای در حوزه اقتصاد، بازار سرمایه، ارز دیجیتال، طلا، دلار و مسائل کلان اقتصادی هستید.

        وظیفه شما خلاصه‌سازی خبری است که در ادامه آمده. خلاصه باید حداکثر **دو جمله** باشد و فقط مهم‌ترین و تأثیرگذارترین نکات اقتصادی را پوشش دهد.

        🟡 موارد زیر در اولویت توجه شما هستند:
        - هر نوع اشاره به بازار بورس، دلار، طلا، ارز دیجیتال
        - واژگان و مفاهیمی مانند: جنگ، تحریم، ورشکستگی، زیان، سود، تورم، رکود، صادرات، واردات، کسری بودجه، بهره بانکی، نرخ ارز، سیاست پولی، سیاست مالی، تصمیمات بانک مرکزی، بحران مالی و سیاسی
        - هر گونه اشاره به شرکت‌ها یا نمادهای بورسی (در این صورت، حتماً نام آن‌ها را در خلاصه بیاور)
        - اخباری که بر بازارهای مالی ایران یا جهان تأثیرگذار هستند

        🔴 توجه:
        اگر متن خبر **فاقد محتوای واقعی یا قابل تحلیل باشد** (مثلاً خالی است یا فقط تیتر تکراری است)، فقط بنویس:
        «خبر فاقد محتوای قابل تحلیل است.»

        حال خبر زیر را با دقت بررسی و سپس خلاصه کن:

        خبر:
        {content}
        """
    )
    chain = prompt | llm
    response = call_chain_with_backoff(chain, {'content': content})
    return response.content.strip() if hasattr(response, 'content') else str(response).strip()


def summarize(state: NewsState) -> NewsState:
    """خلاصه‌سازی خبرها با در نظر گرفتن کش"""

    logger.info("Summarizing articles (batch size: %d)", BATCH_SIZE)
    cache = state.get('cache', {})

    for art in state['articles'][:50]:
        content = art['content']
        link = art['link']
        h = art['hash']

        if 'summary' in cache.get(link, {}):
            logger.info(f"Skipping already summarized article: {link}")
            continue

        try:
            summary_text = summarize_article(content)
            cache_entry = cache.setdefault(link, {})
            cache_entry.update({
                'hash': h,
                'summary': summary_text
            })
        except Exception as e:
            logger.error(f"Failed to summarize article {link}: {str(e)}")
            cache_entry = cache.setdefault(link, {})
            cache_entry.update({
                'hash': h,
                'summary': 'Error in summarization'
            })

    state['cache'] = cache
    return state
