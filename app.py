import pandas as pd
import numpy as np

from sidebar import *
from setup import *
from charts import *
from calls import *

def main():
    alter_default_CSS()
    data = load_reference_tables()

    columnA, columnB = st.columns([0.9,1])
    with columnA:
        token_A = get_sidebar_selections(data)
        urls_A = setup_request_A(token_A)
        df = make_batch_request(urls_A)
        st.write(f"#### Annual {token_A['direction']}s by Country (Top 10)")
        df, graphed_countries = format_chart_data(df, token_A)
        chart = create_linechart_A(df, token_A)
        chart

    with columnB:
        token_B = create_commodity_token(data, token_A, graphed_countries)
        urls_B = setup_request_B(token_B)
        df = make_batch_request(urls_B)
        st.write(f"#### Top Aggregated {token_A['direction']}s of Graphed Countries ({token_B['years'][1]})")
        create_top_commodity_column(df, token_A, token_B)

    alter_default_CSS()
    display_API_calls(urls_A + urls_B)

if __name__ == "__main__":
    main()
