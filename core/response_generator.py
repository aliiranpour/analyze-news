from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from utils.llm import get_llm
import os


llm = get_llm()

def generate_analysis(symbol: str, matching_news: list) -> str:


    combined = "\n".join([
        f"خبر: {n['summary']} | تاثیر: {n['impact']}"
        for n in matching_news
    ])

    prompt_template = ChatPromptTemplate.from_template(
        f"""
        شما یک تحلیلگر حرفه‌ای اقتصادی هستید. بر اساس مجموعه‌ای از خلاصه اخبار و تحلیل‌های زیر که مربوط به نماد 
        «{symbol}» هستند، یک تحلیل دقیق، مستند و کاربردی برای کاربر ارائه دهید.

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
