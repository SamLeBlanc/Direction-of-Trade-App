import streamlit as st
import pandas as pd

# Set default page title and icon
st.set_page_config(page_title='Direction of Trade App', page_icon="🌐")

def load_reference_tables():
    """
    Load reference tables containing coding info for UN countries and trade products.
    Each table is stored as a value in the dictionary that is returned by this funciton.
    ------------------------------------------
    Args:
        None;
    Returns:
        data (dict): dictionary with two dataframes corresponding to codes for countries and commodities
    """
    # Empty dictionary to store reference tables
    data = {}

    # Note the encoding to deal with troublesome characters in country names
    data['countries'] = pd.read_csv("data/coded_countries.csv", encoding="ISO-8859-1")
    data['products']  = pd.read_csv("data/coded_products.csv",  encoding="ISO-8859-1")

    return data

def alter_default_CSS():
    """
    Slightly alter the default Streamlit CSS to change the appearance of the dashbaord.
    Changes are slight, such as shrinking whitespace, changing colors, padding, etc.
    CSS classes are identified by an alphanumeric code that is highly subject to change(!!)
    ----------------------------------------
    Args: None; Returns: None;
    """
    # Note the alphanumeric CSS class selectors are known to change often, so be aware!
    # Also we set the 'unsafe_allow_html' option to 'true' as this is basically a scripting workaround
    st.markdown("<style> .css-1oe6wy4 { padding: 1rem; width: 25rem; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> .css-12oz5g7 { padding: 1rem 3rem; width: 100%; max-width: 100%; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> [data-baseweb='select'] { margin-top: -45px; } </style>",unsafe_allow_html=True,)
    st.markdown("<style> .css-1oe6wy4 h1  { font-family: 'Rubik', sans-serif; font-size: 1.8em; color: hotpink; -webkit-text-stroke: 1px black; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> .css-1oe6wy4 h2  { font-family: 'Rubik', sans-serif; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> .css-16huue1  { font-family: 'Rubik', sans-serif; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)
    st.markdown("<style> .css-10trblm { font-family: 'Rubik', sans-serif; } </style> ", unsafe_allow_html=True)
