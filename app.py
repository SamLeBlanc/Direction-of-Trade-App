import streamlit as st
import numpy as np
import pandas as pd
import requests
import altair as alt

from sidebar import *
from setup import *
from charts import *
from calls import *

def main():
    alter_default_CSS()
    data = load_reference_tables()
    request_dictionary = create_sidebar(data)
    df = pd.read_pickle("hold.pkl")


    chart = create_chart(df)
    chart
    urls = setup_api_request(request_dictionary)
    show_api_call_button(urls)

if __name__ == "__main__":
    main()
