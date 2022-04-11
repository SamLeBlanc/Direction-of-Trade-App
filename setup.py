import streamlit as st
import pandas as pd

st.title("UN COMTRADE")

def load_reference_tables():
    data = {}
    data['countries'] = pd.read_csv("data/coded_countries.csv", encoding="ISO-8859-1")
    data['products']  = pd.read_csv("data/coded_products.csv",  encoding="ISO-8859-1")
    return data

def alter_default_CSS():
    st.markdown("<style> .css-1oe6wy4 { padding: 1rem; width: 25rem; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> .css-12oz5g7 { padding: 1rem 3rem } </style> ", unsafe_allow_html=True)
    st.markdown("<style> [data-baseweb='select'] { margin-top: -45px; } </style>",unsafe_allow_html=True,)
