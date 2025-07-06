# ui/style.py

import streamlit as st

def set_rtl_style():
    st.markdown("""
        <style>
            @font-face {
                font-family: 'Yekan';
                src: url('./static/YekanBakhFaNum-Black.woff') format('woff');
            }

            html, body, [class^="css"] {
                direction: rtl !important;
                text-align: right !important;
                font-family: 'Yekan' !important;
            }

            .stTextInput > div > input,
            .stTextArea > div > textarea,
            .stButton > button,
            .stExpanderHeader {
                text-align: right !important;
                direction: rtl !important;
                font-family: 'Yekan' !important;
            }
        </style>
    """, unsafe_allow_html=True)
