from langchain_core.prompts import ChatPromptTemplate
from utils.retry import call_chain_with_backoff
from utils.parsers import extract_section , parse_impact, extract_impact_section
from utils.llm import get_llm
from utils.logger import get_logger
from models.news_types import NewsState

# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from models.news_types import NewsState

# logger = get_logger(__name__)


# def analyze(state: 'NewsState') -> 'NewsState':
#     """
#     تحلیل خلاصه‌های خبری برای استخراج نمادهای بورسی، کلیدواژه‌ها و تأثیر کوتاه‌مدت.
#     """

#     cache = state.get('cache', {})
#     summaries = state.get('summaries', [])
#     for summary_entry in summaries:
#         summary_text = summary_entry.get('summary', '')
#         link = summary_entry.get('link')

#         try:
#             analysis = analyze_summary(summary_text)
#             cache_entry = cache.setdefault(link, {})
#             cache_entry.update({
#                 'symbols': analysis['symbols'],
#                 'keywords': analysis['keywords'],
#                 'impact_stock': analysis['impact_stock'],
#             })
#             summary_entry.update(cache_entry)
#         except Exception as e:
#             logger.error(f"Failed to analyze summary for {link}: {str(e)}")
#             summary_entry.update({
#                 'symbols': [],
#                 'keywords': [],
#                 'impact': '',
#             })

#     state['cache'] = cache
#     state['summaries'] = summaries
#     return state


# def analyze_summary(summary: str) -> dict:
#     llm =get_llm()
#     prompt = ChatPromptTemplate.from_template(
#         """
#         با توجه به خلاصه خبر اقتصادی زیر:

#         1. تأثیر کوتاه‌مدت روی نمادها و دارایی‌های مالی را تشخیص بده (فقط یکی از: مثبت، منفی یا خنثی).
#         2. فقط از **نمادهای رسمی بورس ایران** برای شرکت‌های بورسی استفاده کن (مثال: فولاد، خساپا، وبصادر).
#         3. در صورت تأثیر خبر بر سایر دارایی‌ها مانند طلا، دلار و ارزهای دیجیتال نیز، آن‌ها را در لیست نمادها وارد کن (مثال: طلا، دلار، بیت‌کوین).
#         4. اگر خبر مربوط به یک صنعت خاص است (مثلاً بانک، خودروسازی، غذا)، تمام نمادهای مربوط به آن صنعت را تأثیرپذیر در نظر بگیر.
#         5. حداقل ۳ کلیدواژه مالی مهم استخراج کن.
#         6. برای اخبار کلان (مثل جنگ، تحریم، توافق)، تأثیر آن بر شاخص کل بورس را نیز در نظر بگیر.

#         📌 توجه:
#         - فقط برای شرکت‌های بورسی، از **نمادهای رسمی بورس ایران** استفاده کن. هیچ نماد ساختگی یا اشتباهی تولید نکن.
#         - برای سایر دارایی‌ها مانند طلا، دلار و ارزهای دیجیتال، در صورت تأثیرپذیری آن‌ها را به‌عنوان نماد ذکر کن.
#         - اگر نمادی مرتبط نیست، فیلد مربوطه را خالی بگذار.

#         فرمت خروجی:
#         نمادها: [لیست نمادها مانند: فولاد, خساپا]
#         کلیدواژه‌ها: [لیست کلیدواژه‌ها]
#         تأثیر: [مثبت/منفی/خنثی]

#         خلاصه خبر:
#         {summary}
#         """
#     )
#     chain = prompt | llm
#     response = call_chain_with_backoff(chain, {'summary': summary})
#     text = response.content.strip()
#     res = {
#         'symbols': [sym for sym in parse_list(extract_section(text, "نمادها"))] or 'nothing found',
#         'keywords': parse_list(extract_section(text, "کلیدواژه‌ها")),
#         'impact_stock': parse_impact(extract_section(text, "تأثیر"))
#     }
#     return res

# def analyze_impact(state: 'NewsState') -> 'NewsState':
#     """
#     تحلیل شدت تأثیر خبر روی نمادهای از پیش تعیین‌شده.
#     """

#     summaries = state.get('summaries', [])
#     cache = state.get('cache', {})
#     logger = get_logger()

#     for entry in summaries:
#         summary_text = entry.get('summary', '')
#         link = entry.get('link')
#         symbols = entry.get('symbols', []) 

#         print('analyze:', symbols)

#         if not symbols:
#             continue 

#         try:
#             impact_result = analyze_impact_on_symbols(summary_text, symbols)
#             cache_entry = cache.setdefault(link, {})
#             cache_entry.update({
#                 'impact_stock': impact_result['impact_stock'],  # dict: نماد → نوع اثر
#             })
#             entry.update(cache_entry)
#         except Exception as e:
#             logger.error(f"Failed to analyze impact for {link}: {str(e)}")
#             entry.update({'impact_stock': {sym: 'نامشخص' for sym in symbols}})

#     state['cache'] = cache
#     state['summaries'] = summaries
#     return state

def analyze_impact(state: 'NewsState') -> 'NewsState':
    """
    تحلیل شدت تأثیر خبر روی نمادها بر اساس خلاصه هر خبر.
    """
    cache = state.get('cache', {})
    logger = get_logger()

    for link, entry in cache.items():
        summary_text = entry.get('summary')
        symbols = entry.get('symbols')

        if not summary_text or not symbols:
            continue  

        print('🔍 analyzing:', link, symbols)

        impact_dict = {} 

        for sym in symbols:
            try:
                impact_result = analyze_impact_on_symbols(summary_text, sym)
                impact_dict[sym] = impact_result['impact_stock']  

            except Exception as e:
                logger.error(f"❌ Failed to analyze impact for {link}: {str(e)}")
                impact_dict[sym] = 'نامشخص'
        
        entry['impact_stock'] = impact_dict  

    state['cache'] = cache
    return state

def analyze_impact_on_symbols(summary: str, symbol: str) -> dict:
    llm = get_llm()
    prompt = ChatPromptTemplate.from_template(
        """
            شما یک تحلیل‌گر حرفه‌ای بازار سرمایه هستید که بر اساس خبرهای اقتصادی، تأثیر آن‌ها را به‌صورت دقیق و منطقی بر نمادهای بورسی تحلیل می‌کنید.

            ### وظیفه:
            بر اساس خلاصه خبر زیر و نماد ارائه‌شده، یک تحلیل جامع و واقع‌بینانه از اثر این خبر بر نماد مذکور بنویسید. تحلیل باید با در نظر گرفتن ماهیت صنعت نماد، وضعیت فعلی اقتصاد، جهت و شدت اثر خبر (مثلاً تهدید، فرصت، یا خنثی)، و هرگونه آثار کوتاه‌مدت یا بلندمدت انجام شود.

            حتماً به نکات زیر توجه کنید:
            1. آیا این خبر به‌طور مستقیم یا غیرمستقیم بر فعالیت‌ها یا سودآوری نماد تأثیر دارد؟
            2. آیا این تأثیر در کوتاه‌مدت است یا بلندمدت؟
            3. آیا ریسک یا فرصت جدیدی برای نماد ایجاد می‌شود؟
            4. در تحلیل از استدلال دقیق و مبتنی بر مفروضات منطقی استفاده کنید و از تکرار کلیشه‌ای اجتناب نمایید.
            5. تحلیل باید کاملاً مرتبط با اطلاعات موجود در خبر و حوزه فعالیت نماد باشد.

            ### فقط یکی از گزینه‌های زیر را به عنوان نوع اثر انتخاب کن:
            - مثبت
            - منفی
            - خنثی

            ### خلاصه خبر:
            {summary}

            ### نماد:
            {symbol}

            ### فرمت دقیق پاسخ:

            تأثیر: [یکی از گزینه‌های بالا]
پ
        """
    )

    chain = prompt | llm
    response = call_chain_with_backoff(chain, {
        'summary': summary,
        'symbol': symbol
    })
    print(f"📨 LLM response for {symbol}:\n{response.content}")
    text = response.content.strip()
    impact_text = extract_impact_section(text)
    impact = parse_impact(impact_text)

    return {'impact_stock': impact }
