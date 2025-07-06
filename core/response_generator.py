# core/response_generator.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.avalapis.ir/v1")
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "deepseek-chat")

llm = ChatOpenAI(
    model_name=MODEL_NAME,
    openai_api_base=OPENAI_API_BASE,
    openai_api_key=OPENAI_API_KEY,
    temperature=0.0
)

def generate_analysis(symbol: str, matching_news: list) -> str:
    combined = "\n".join([
        f"خبر: {n['summary']} | کلیدواژه‌ها: {', '.join(n['keywords'])} | تاثیر: {n['impact']}"
        for n in matching_news
    ])

    prompt_template = ChatPromptTemplate.from_template(
        f"""
        شما یک تحلیلگر حرفه‌ای اقتصادی هستید. بر اساس مجموعه‌ای از خلاصه اخبار و تحلیل‌های زیر که مربوط به نماد «{symbol}» هستند، یک تحلیل دقیق، مستند و کاربردی برای کاربر ارائه دهید.

        تحلیل شما باید شامل بخش‌های زیر باشد:
        1. **روند کلی احتمالی نماد {symbol}** در کوتاه‌مدت بر اساس داده‌های ارائه‌شده
        2. **ریسک‌ها و تهدیدهای احتمالی**
        3. **فرصت‌ها و نکات مثبت بالقوه**
        4. در پایان، یک **جمع‌بندی نهایی** بنویس و تأثیر کلی اخبار امروز بر نماد {symbol} را با یکی از این سه گزینه مشخص کن: **مثبت**، **منفی** یا **خنثی**.

        داده‌های تحلیل:
        {combined}
        """
    )
    chain = prompt_template | llm
    response = chain.invoke({"symbol": symbol, "combined": combined})
    return response.content if hasattr(response, 'content') else str(response)
