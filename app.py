import pandas as pd
import numpy as np
from st_btn_select import st_btn_select

from sidebar import *
from setup import *
from charts import *
from calls import *


def format_chart_data(df, token):
    # Only include data for the trade direction being graphed
    df = df[df.rgDesc == token['direction']]

    # Get 10 countries to be graphed
    df_plot = df[df.yr == max(df.yr)]
    df_plot = df_plot.sort_values(by="TradeValue", ascending=False)
    if token['direction'] in ['Import','Export']:
        df_plot = df_plot.iloc[0:10,:].reset_index()
    else:
        df_plot = pd.concat([df_plot.iloc[0:5,:], df_plot.iloc[-5:,:]]).reset_index()

    graphed_countries = list(df_plot.rtTitle)

    # Filter dataframe to only include the countries being graphed
    df = df[df['rtTitle'].isin(graphed_countries)]

    # Format axis and tooltip labels
    df['yr'] = pd.to_datetime(df['yr'], format="%Y")
    df['tool'] = df['TradeValue'].apply(lambda row: format_number_short(row))

    return df, graphed_countries


def main():
    alter_default_CSS()
    data = load_reference_tables()
    token = create_sidebar(data)
    df, urls = setup_api_request(token)
    col1, col2 = st.columns([0.9,1])
    with col1:
        st.write(f"#### Annual {token['direction']}s by Country (Top 10)")
        df, graphed_countries = format_chart_data(df, token)
        chart = create_chart(df, token)
        chart

    with col2:
        coded_countries = data['countries']
        dat = coded_countries[coded_countries['country'].isin(graphed_countries[0:5])]
        reporter_codes = dat.code.values

        token2 = {
            'reporter_codes' : reporter_codes,
            'parter_codes' : token['parter_codes'],
            'direction' : token['direction'],
            'years' : token['years'],
            'commodity_codes' : 'AG2'
        }
        df = get_commodity_data(token2)
        df = df.groupby(by=["cmdDescE"]).sum().reset_index()
        df = df[['cmdDescE','TradeValue']].sort_values(by='TradeValue', ascending=False)
        s = ''

        st.write(f"#### Top Aggregated {token['direction']}s of Graphed Countries ({token2['years'][1]})")
        for index, row in df[:10].iterrows():
            num = '{:,}'.format(row.TradeValue)
            new_title = f'''
            <span style="font-family:sans-serif; color:Green; font-size: 22px; font-weight: 900;">${num}</span>
            <span style="color:#0E1117">-</span>
            <span style="font-family:sans-serif; color:White; font-size: 16px;">{row.cmdDescE}</span>
            '''
            st.markdown(new_title, unsafe_allow_html=True)


    alter_default_CSS()
    for u in urls:
        st.write(u)

if __name__ == "__main__":
    main()
