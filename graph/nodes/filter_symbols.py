from typing import TYPE_CHECKING
from utils.logger import get_logger
from utils.parsers import parse_symbols  
from langchain_core.prompts import ChatPromptTemplate
from utils.llm import get_llm
from utils.retry import call_chain_with_backoff
from utils.parsers import parse_list, extract_section
if TYPE_CHECKING:
    from models.news_types import NewsState  

logger = get_logger(__name__)
llm = get_llm()

# def find_symbols(state: 'NewsState') -> 'NewsState':

    
#     cache = state.get('cache' , {})
#     summarize = state.get('summaries', [])
#     valid_symbols = list(state.get('valid_symbol_names', []))[:200]


#     for summary in summarize:
#         prompt = ChatPromptTemplate.from_template(  
#             """
#                 شما یک تحلیل‌گر خبره بازار سرمایه هستید.

#                 در ادامه یک خبر اقتصادی خلاصه‌شده و لیستی از نمادهای معتبر بورسی ایران ارائه می‌شود. وظیفه شما این است که مشخص کنید این خبر روی کدام نمادها تأثیرگذار است.
#                 ### لطفاً تمام جنبه‌های زیر را برای تحلیل در نظر بگیرید:

#                 1. **تأثیر مستقیم:** آیا خبر به‌طور مستقیم به حوزه فعالیت شرکت مربوط است؟ (مثلاً خبر درباره قیمت فولاد برای نمادهای فلزی)
#                 2. **تأثیر غیرمستقیم:** آیا از طریق زنجیره تأمین، مصرف، یا صنعت بالادستی/پایین‌دستی ممکن است اثر بگذارد؟
#                 3. **تأثیر مالی:** آیا درآمد، هزینه، سود، یا بودجه شرکت به نحوی تحت‌تأثیر قرار می‌گیرد؟
#                 4. **تأثیر روانی و انتظارات بازار:** آیا خبر باعث خوش‌بینی یا بدبینی نسبت به آن صنعت یا شرکت می‌شود؟
#                 5. **تأثیر سیاسی یا مقرراتی:** آیا سیاست‌های دولتی، مالیاتی، یارانه‌ای یا صادراتی/وارداتی در خبر ممکن است روی نماد اثر بگذارد؟
#                 6. **تأثیر ارزی:** آیا شرکت صادرات‌محور یا واردات‌محور است و خبر شامل تغییرات نرخ ارز یا سیاست‌های ارزی است؟
#                 7. **تأثیر ساختاری:** آیا خبر درباره زیرساخت‌ها، پروژه‌های عمرانی، بودجه عمرانی، انرژی، حمل‌ونقل و غیره است که ممکن است به‌صورت بلندمدت اثر بگذارد؟
#                 8. **تأثیر بخشی/صنعتی:** آیا خبر روی کل یک صنعت یا گروه خاص اثر می‌گذارد؟ (مثلاً نرخ بهره برای بانک‌ها)
#                 9. **وابستگی به نهاد یا سازمان:** آیا شرکتی به نهادی که در خبر ذکر شده مرتبط است؟ (مثلاً شرکت‌های زیرمجموعه دولت)
#                 10. **احتمال تأثیر بلندمدت یا غیرقطعی:** حتی اگر اثر کوتاه‌مدت ندارد، آیا در بلندمدت یا در سناریوهای خاص ممکن است اثرگذار باشد؟

#                 ### خلاصه خبر:
#                 {summary}

#                 ### لیست نمادهای بورسی:
#                 {valid_symbols}

#                 ### خروجی مورد انتظار:
#                 لیستی از نمادهایی که تحت تأثیر این خبر قرار می‌گیرند، به همراه دلیل کوتاهی برای هر مورد.
#                 فرمت خروجی:
#                 نمادها: [نام نماد]

#                 اگر هیچ نمادی مرتبط نیست، فقط یک لیست برگردان 
#             """
#         )

#         chain = prompt | llm 
#         response = call_chain_with_backoff(chain, { 'summary': summary , 'valid_symbols' : valid_symbols })
#         text = response.content.strip()
#         print('find symbols: ', parse_list(extract_section(text, "نمادها")) )
#         state['symbols'] = [parse_list(extract_section(text, "نمادها"))] or 'nothing found'

#     return state


def find_symbols(state: 'NewsState') -> 'NewsState':
    cache = state.get('cache', {})
    valid_symbols = list(state.get('valid_symbol_names', []))[:200]

    for link, entry in cache.items():
        if 'summary' not in entry:
            continue  # اگر خلاصه وجود ندارد، رد شو

        if 'symbols' in entry:
            continue  # اگر قبلاً نمادها استخراج شده‌اند، رد شو

        summary = entry['summary']

        try:
            prompt = ChatPromptTemplate.from_template("""
                 شما یک تحلیل‌گر خبره بازار سرمایه هستید.

                 در ادامه یک خبر اقتصادی خلاصه‌شده و لیستی از نمادهای معتبر بورسی ایران ارائه می‌شود. وظیفه شما این است که مشخص کنید این خبر روی کدام نمادها تأثیرگذار است.
                 ### لطفاً تمام جنبه‌های زیر را برای تحلیل در نظر بگیرید:

                 1. **تأثیر مستقیم:** آیا خبر به‌طور مستقیم به حوزه فعالیت شرکت مربوط است؟ (مثلاً خبر درباره قیمت فولاد برای نمادهای فلزی)
                 2. **تأثیر غیرمستقیم:** آیا از طریق زنجیره تأمین، مصرف، یا صنعت بالادستی/پایین‌دستی ممکن است اثر بگذارد؟
                 3. **تأثیر مالی:** آیا درآمد، هزینه، سود، یا بودجه شرکت به نحوی تحت‌تأثیر قرار می‌گیرد؟
                 4. **تأثیر روانی و انتظارات بازار:** آیا خبر باعث خوش‌بینی یا بدبینی نسبت به آن صنعت یا شرکت می‌شود؟
                 5. **تأثیر سیاسی یا مقرراتی:** آیا سیاست‌های دولتی، مالیاتی، یارانه‌ای یا صادراتی/وارداتی در خبر ممکن است روی نماد اثر بگذارد؟
                 6. **تأثیر ارزی:** آیا شرکت صادرات‌محور یا واردات‌محور است و خبر شامل تغییرات نرخ ارز یا سیاست‌های ارزی است؟
                 7. **تأثیر ساختاری:** آیا خبر درباره زیرساخت‌ها، پروژه‌های عمرانی، بودجه عمرانی، انرژی، حمل‌ونقل و غیره است که ممکن است به‌صورت بلندمدت اثر بگذارد؟
                 8. **تأثیر بخشی/صنعتی:** آیا خبر روی کل یک صنعت یا گروه خاص اثر می‌گذارد؟ (مثلاً نرخ بهره برای بانک‌ها)
                 9. **وابستگی به نهاد یا سازمان:** آیا شرکتی به نهادی که در خبر ذکر شده مرتبط است؟ (مثلاً شرکت‌های زیرمجموعه دولت)
                 10. **احتمال تأثیر بلندمدت یا غیرقطعی:** حتی اگر اثر کوتاه‌مدت ندارد، آیا در بلندمدت یا در سناریوهای خاص ممکن است اثرگذار باشد؟

                 ### خلاصه خبر:
                 {summary}

                 ### لیست نمادهای بورسی:
                 {valid_symbols}

                ✳️ فرمت خروجی:
                    لطفاً **فقط** یک خط با فرمت دقیق زیر تولید کنید، بدون هیچ متن اضافی:

                    نمادها: ["نماد1", "نماد2", "نماد3"]

                    اگر هیچ نمادی مرتبط نیست، بنویس:
                    نمادها: []
            """)

            chain = prompt | llm 
            response = call_chain_with_backoff(chain, {
                'summary': summary,
                'valid_symbols': valid_symbols
            })

            text = response.content.strip()
            extracted = parse_list(extract_section(text, "نمادها"))
            cleaned_symbols = [sym.strip("'\" ") for sym in extracted if sym.strip("'\" ")]

            print(f"🔎 find symbols for {link} →", extracted)

            entry['symbols'] = cleaned_symbols

        except Exception as e:
            logger.error(f"Error extracting symbols for {link}: {str(e)}")
            entry['symbols'] = []

    state['cache'] = cache
    return state
