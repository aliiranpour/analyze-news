from langchain_core.prompts import ChatPromptTemplate
from utils.retry import call_chain_with_backoff
from utils.parsers import extract_section, parse_list, parse_impact
from utils.llm import get_llm
from utils.logger import get_logger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.news_types import NewsState

logger = get_logger(__name__)


def analyze(state: 'NewsState') -> 'NewsState':
    """
    تحلیل خلاصه‌های خبری برای استخراج نمادهای بورسی، کلیدواژه‌ها و تأثیر کوتاه‌مدت.
    """

    cache = state.get('cache', {})
    summaries = state.get('summaries', [])
    for summary_entry in summaries:
        summary_text = summary_entry.get('summary', '')
        link = summary_entry.get('link')

        try:
            analysis = analyze_summary(summary_text)
            cache_entry = cache.setdefault(link, {})
            cache_entry.update({
                'symbols': analysis['symbols'],
                'keywords': analysis['keywords'],
                'impact_stock': analysis['impact_stock'],
            })
            summary_entry.update(cache_entry)
        except Exception as e:
            logger.error(f"Failed to analyze summary for {link}: {str(e)}")
            summary_entry.update({
                'symbols': [],
                'keywords': [],
                'impact': '',
            })

    state['cache'] = cache
    state['summaries'] = summaries
    return state


def analyze_summary(summary: str) -> dict:
    llm =get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
        با توجه به خلاصه خبر اقتصادی زیر:

        1. تأثیر کوتاه‌مدت روی نمادها و دارایی‌های مالی را تشخیص بده (فقط یکی از: مثبت، منفی یا خنثی).
        2. فقط از **نمادهای رسمی بورس ایران** برای شرکت‌های بورسی استفاده کن (مثال: فولاد، خساپا، وبصادر).
        3. در صورت تأثیر خبر بر سایر دارایی‌ها مانند طلا، دلار و ارزهای دیجیتال نیز، آن‌ها را در لیست نمادها وارد کن (مثال: طلا، دلار، بیت‌کوین).
        4. اگر خبر مربوط به یک صنعت خاص است (مثلاً بانک، خودروسازی، غذا)، تمام نمادهای مربوط به آن صنعت را تأثیرپذیر در نظر بگیر.
        5. حداقل ۳ کلیدواژه مالی مهم استخراج کن.
        6. برای اخبار کلان (مثل جنگ، تحریم، توافق)، تأثیر آن بر شاخص کل بورس را نیز در نظر بگیر.

        📌 توجه:
        - فقط برای شرکت‌های بورسی، از **نمادهای رسمی بورس ایران** استفاده کن. هیچ نماد ساختگی یا اشتباهی تولید نکن.
        - برای سایر دارایی‌ها مانند طلا، دلار و ارزهای دیجیتال، در صورت تأثیرپذیری آن‌ها را به‌عنوان نماد ذکر کن.
        - اگر نمادی مرتبط نیست، فیلد مربوطه را خالی بگذار.

        فرمت خروجی:
        نمادها: [لیست نمادها مانند: فولاد, خساپا]
        کلیدواژه‌ها: [لیست کلیدواژه‌ها]
        تأثیر: [مثبت/منفی/خنثی]

        خلاصه خبر:
        {summary}
        """
    )
    chain = prompt | llm
    response = call_chain_with_backoff(chain, {'summary': summary})
    text = response.content.strip()
    res = {
        'symbols': [sym for sym in parse_list(extract_section(text, "نمادها"))] or 'nothing found',
        'keywords': parse_list(extract_section(text, "کلیدواژه‌ها")),
        'impact_stock': parse_impact(extract_section(text, "تأثیر"))
    }
    return res

