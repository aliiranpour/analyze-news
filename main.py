# app.py

import os
import json
import streamlit as st
from utils.setting import CACHE_FILE
from core.response_generator import generate_analysis
from ui.styles import set_rtl_style
from graph.nodes.load_cache import load_cache 
from graph.economic_graph import run_pipeline_graph

st.set_page_config(page_title="داشبورد اخبار نمادها", layout="wide")
set_rtl_style()

# اجرای خودکار گراف هنگام ورود به صفحه
if "pipeline_ran" not in st.session_state:
    st.session_state["pipeline_ran"] = False

if not st.session_state["pipeline_ran"]:
    with st.spinner("📡 در حال دریافت و بروزرسانی اخبار... لطفاً شکیبا باشید."):
        run_pipeline_graph()
    st.session_state["pipeline_ran"] = True
    st.success("✅ اخبار با موفقیت بروزرسانی شدند.")
    st.rerun()  # صفحه را مجدداً بارگذاری می‌کند تا کش جدید خوانده شود


st.title("🔍 داشبورد جستجوی اخبار بورسی")

symbol_input = st.text_input(
    "نام نماد را وارد کنید (مثال: فولاد)", value="",
    help="نام نماد بورسی را به حروف فارسی وارد کنید"
)

state = {'cache': {}}
state = load_cache(state)
cache = state['cache']

if symbol_input:
    symbol = symbol_input.strip()
    matching = []
    for link, info in cache.items():
        syms = info.get('symbols') or []
        if symbol in syms:
            matching.append({
                'link': link,
                'summary': info.get('summary', ''),
                'keywords': info.get('keywords', []),
                'impact': info.get('impact_stock', '')
            })

    if not matching:
        st.warning(f"هیچ خبری برای نماد '{symbol}' در کش یافت نشد.")
    else:
        st.success(f"{len(matching)} خبر مرتبط با نماد '{symbol}' یافت شد.")
        for news in matching:
            with st.expander(news['link']):
                st.markdown(f"**خلاصه خبر:** {news['summary']}")
                st.markdown(f"**تأثیر روی نماد:** {news['impact']}")

        if st.button("📊 تحلیل کلی نماد توسط مدل زبانی"):
            with st.spinner("در حال تحلیل توسط مدل زبانی..."):
                result = generate_analysis(symbol, matching)
            st.markdown("---")
            st.subheader("📝 تحلیل مدل زبانی")
            st.write(result)
else:
    st.info("لطفاً نام نماد را وارد کنید تا اخبار مرتبط نمایش داده شود.")

st.markdown("---")
st.markdown("© 2025 سامانه تحلیل اخبار بورس")
