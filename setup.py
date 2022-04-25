import streamlit as st
import pandas as pd

st.set_page_config(page_title='Trade', page_icon=":shark:")
st.title("UN COMTRADE")
subtitle = st.empty()

def create_subtitle(df):
        tf = {"1":"Import", "2":"Export", "all":"Net Export"}
        direction = tf[request_dictionary['direction']]

        df = data['countries']
        r = request_dictionary['r_codes'][0]
        r2 = df[df.code == r]['country'].values[0]

        p = request_dictionary['p_codes'][0]
        p2 = df[df.code == p]['country'].values[0]

        y0 = request_dictionary['years'][0]
        y1 = request_dictionary['years'][1]

        subtitle.text(f"Currently showing the {direction}s from {r2} to {p2} between {y0} and {y1}.")


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
    st.markdown("<style> .css-12oz5g7 { padding: 1rem 3rem; width: 100%; max-width: 100%; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> [data-baseweb='select'] { margin-top: -45px; } </style>",unsafe_allow_html=True,)
    st.markdown("<style> .css-1oe6wy4 h1  { font-family: 'Rubik', sans-serif; font-size: 1.8em; color: hotpink; -webkit-text-stroke: 1px black; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> .css-1oe6wy4 h2  { font-family: 'Rubik', sans-serif; } </style> ", unsafe_allow_html=True)
    st.markdown("<style> .css-16huue1  { font-family: 'Rubik', sans-serif; } </style> ", unsafe_allow_html=True)
