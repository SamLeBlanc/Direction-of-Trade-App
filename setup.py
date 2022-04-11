import streamlit as st
import pandas as pd

st.title("UN COMTRADE")

def load_reference_tables():
    """
    Load reference tables containing info on UN country and commodity codes.
    Each table is stored as a value in a dictionary that is returned by this funciton.
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
    CSS classes are identified by alphanumeric code that is highly subject to change(!!)
    ----------------------------------------
    Args: None; Returns: None;
    """
    # Note the alphanumeric CSS class selectors, which are known to change often, so be aware!
    # Also note that we set the 'unsafe_allow_html' option to 'true' as this is basically a scripting hack
    st.markdown("<style> .css-1oe6wy4 { padding: 1rem; width: 25rem; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> .css-12oz5g7 { padding: 1rem 3rem } </style> ", unsafe_allow_html=True)
    st.markdown("<style> [data-baseweb='select'] { margin-top: -45px; } </style>",unsafe_allow_html=True,)
