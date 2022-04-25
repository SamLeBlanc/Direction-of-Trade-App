import pandas as pd
import numpy as np
from st_btn_select import st_btn_select

from sidebar import *
from setup import *
from charts import *
from calls import *



def main():
    alter_default_CSS()
    data = load_reference_tables()
    request_dictionary = create_sidebar(data)
    urls = setup_api_request(request_dictionary)
    create_subtitle(df)
    df = pd.read_pickle("hold.pkl")
    df = calculate_net_exports(df)

    col1, col2 = st.columns(2)
    with col1:
        chart, top_cont = create_chart(df, request_dictionary)
        chart
        s = (i for i in top_cont[0:5])
        selection = st_btn_select(s)

    with col2:
        pass
        
    alter_default_CSS()
    show_api_call_button(urls)

if __name__ == "__main__":
    main()
