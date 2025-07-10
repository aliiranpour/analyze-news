

## 📄 `README.md` (English Version)

````markdown
# 📊 Economic News Impact Analyzer

A modular LLM-powered system for summarizing and analyzing economic news to assess its effect on stock symbols in the Iranian market. Built with [LangGraph](https://www.langchain.com/langgraph), [LangChain](https://www.langchain.com/), and [Streamlit](https://streamlit.io/), it offers a user-friendly dashboard that extracts and analyzes relevant news to provide insight into stock trends.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/aliiranpour/analyze-news.git
cd analyze-news

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run main.py
````

Create a `.env` file based on `.env.example` and add your OpenAI API key:

```env
OPENAI_API_KEY=your_openai_key_here
```

---

## 🖼️ App Overview

When the app launches:

* You’ll see a clean dashboard with a text input for stock symbol names (e.g., "شستا").
* The system automatically retrieves relevant news headlines, summarizes them using an LLM, and filters them based on their relevance.
![search a symbol](./static/assetes/search_new.gif)
* When you click the **"Analyze with LLM"** button, a detailed GPT-based analysis is generated for the selected stock.
![search a symbol](./static/assetes/analyze.gif)
---

## 🧪 Example Output

> 🔎 Symbol: **شستا**
> News Count: 5
> ✅ Model Analysis: Based on tax relief, industrial support policies, and stable exports, the short-term outlook is **positive**.

---

## 🛠️ Technologies Used

* **Python 3.11+**
* **LangGraph** – LLM orchestration
* **LangChain** – prompt & agent management
* **Streamlit** – user interface
* **OpenAI API** – for summarization & analysis
* **BeautifulSoup / feedparser** – for news crawling

---

## 📁 Project Structure

```plaintext
economic-news-analyzer/
├── graph/
│   ├── economic_graph.py         # LangGraph flow
│   └── nodes/                    # Each graph node (summarize, analyze, etc.)
├── core/
│   └── response_generator.py     # Final LLM-based response composer
├── ui/
│   └── styles.py                 # Custom Streamlit styles
├── models/
│   └── news_types.py             # Dataclasses for sentiment & impact
├── utils/
│   ├── fetch_news.py, summarizer.py, cache_handler.py, etc.
├── main.py                       # Streamlit entry point
├── requirements.txt
└── .env                          # API key config
```

---

## 🔄 Graph Flow

1. `fetch_symbols` → Load stock names.
2. `load_cache` → Skip previously analyzed news.
3. `fetch_rss` / `fetch_news` → Get headlines.
4. `summarize` → Use LLM to create a brief summary.
5. `analyze` → Extract stock symbols, keywords, and effects.
6. `filter_symbols` → Keep only relevant news.
7. `save_cache` → Store in JSON cache.
8. `print_cache` → Display in the UI.
9. `response_generator` → Final LLM insight per symbol.

---

## ✨ Who Can Use This?

* Investors analyzing the stock market
* Data scientists testing LangGraph
* Researchers building LLM + graph architectures

---

## 📬 Contributing

Fork, star, and PRs are welcome. For questions, open an issue or email:

**[iranpour181@gmail.com](mailto:iranpour181@gmail.com)**


---

## 📄 `README_FA.md` (نسخه فارسی)

```markdown
# 📊 تحلیلگر تأثیر اخبار اقتصادی بر نمادهای بورسی

سامانه‌ای ماژولار مبتنی بر مدل‌های زبانی (LLM) برای دریافت، خلاصه‌سازی و تحلیل اخبار اقتصادی با هدف ارزیابی تأثیر آن‌ها بر نمادهای بورس ایران. این پروژه با استفاده از [LangGraph](https://www.langchain.com/langgraph)، [LangChain](https://www.langchain.com/)، و [Streamlit](https://streamlit.io/) طراحی شده و دارای داشبوردی تعاملی برای نمایش خروجی‌هاست.

---

## 🚀 نحوه اجرا

```bash
git clone https://github.com/aliiranpour/analyze-news.git
cd analyze-news

pip install -r requirements.txt

streamlit run main.py
````

سپس یک فایل `.env` بسازید و کلید OpenAI خود را اضافه کنید:

```env
OPENAI_API_KEY=کلید_API_شما
```

---

## 🖼️ تجربه کاربری

پس از اجرای برنامه:

* صفحه‌ای با فیلد ورود نماد بورس ظاهر می‌شود.
* با وارد کردن نام نماد (مثل "شستا")، اخبار مرتبط از منابع اقتصادی بارگیری و خلاصه‌سازی می‌شود.
![search a symbol](./static/assetes/search_new.gif)
* با کلیک بر دکمه **تحلیل با مدل زبانی**، تحلیل نهایی توسط GPT انجام شده و نمایش داده می‌شود.
![search a symbol](./static/assetes/analyze.gif)

---

## 🧪 نمونه خروجی

نماد: **شستا**
تعداد خبر: ۵
تحلیل مدل: به دلیل کاهش مالیات، حمایت‌های صنعتی و ثبات صادرات، انتظار می‌رود روند نماد در کوتاه‌مدت **مثبت** باشد ✅

---

## 🛠️ تکنولوژی‌های استفاده‌شده

* Python 3.11+
* LangGraph + LangChain
* OpenAI GPT API
* Streamlit
* BeautifulSoup / feedparser

---

## 📁 ساختار پوشه‌ها

```plaintext
economic-news-analyzer/
├── graph/
│   └── nodes/ (گره‌های گراف مانند summarize، analyze، filter و...)
├── core/ → تولید پاسخ نهایی با GPT
├── models/ → تعریف کلاس‌های داده مانند نوع تأثیر
├── utils/ → ابزارهای کمکی مثل کش، خلاصه‌سازی، LLM
├── ui/ → استایل Streamlit
├── main.py → فایل اصلی اجرا
└── .env → کلید API
```

---

## 🔄 جریان داده‌ها

۱. بارگیری لیست نمادها
۲. فراخوانی کش
۳. دریافت خبر (RSS و HTML)
۴. خلاصه‌سازی با GPT
۵. تحلیل و استخراج نماد و اثر
۶. فیلتر کردن خبرهای مرتبط
۷. ذخیره در کش
۸. نمایش در داشبورد
۹. تحلیل نهایی مدل زبانی

---

## 👥 مناسب برای

* تحلیل‌گران بازار سرمایه
* توسعه‌دهندگان علاقه‌مند به LangGraph
* پژوهشگران NLP و مدل‌های زبانی

---

## 📬 ارتباط و مشارکت

خوشحال می‌شویم پروژه را فورک یا ستاره کنید و در توسعه مشارکت نمایید.
در صورت سؤال:
📧 [iranpour181@gmail.com](mailto:iranpour181@gmail.com)


