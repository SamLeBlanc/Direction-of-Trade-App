import pandas as pd
import altair as alt
import numpy as np
import streamlit as st

def format_number_short(num):
    """
    Format a number to have 'short scientific format' or a single digit number and letter representing order.
    For example, 5,600,000,000 -> 5.6B and 1,200,000 -> 1.2M and 8320 -> 8.3K
    ------------------------------------------------------
    Args:
        num (float): number to be converted to short format
    Returns:
        num (string): formatted number
    """
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '$%.1f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def create_top_commodity_column(df, token, token_B):
    df = df.groupby(by=["cmdDescE"]).sum().reset_index()
    df = df[['cmdDescE','TradeValue']].sort_values(by='TradeValue', ascending=False)
    s = ''

    for index, row in df[:10].iterrows():
        num = '{:,}'.format(row.TradeValue)
        new_title = f'''
        <span style="font-family:sans-serif; color:Green; font-size: 22px; font-weight: 900;">${num}</span>
        <span style="color:#0E1117">-</span>
        <span style="font-family:sans-serif; color:White; font-size: 16px;">{row.cmdDescE}</span>
        '''
        st.markdown(new_title, unsafe_allow_html=True)



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



def create_linechart_A(df, token_A):
    """
    Creates a line chart (in column A) depicting the changes in annual trade flows by country.
    Chart is an 'interactive' altair chart and is extremely finicky, so be careful when changing.
    -----------------------------------------------------------------------------
    Args:
        df: dataframe of annual trade flow data by country
        token_A (dict): reference information (used for title, etc.) based on original API request
    """
    # Selectors used to display value of nearest hovered data point
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['yr'], empty='none')
    selectors = alt.Chart(df).mark_point().encode(x='yr:T', opacity=alt.value(0)).add_selection(nearest)
    selection = alt.selection_multi(fields=['rtTitle'], bind='legend')

    # Line and Data Points
    line = alt.Chart(df).mark_line().encode(x='yr:T', y='TradeValue:Q',
        color = alt.Color('rtTitle:N', sort=alt.EncodingSortField('TradeValue', op='mean', order='descending')))
    points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

    # Tooltip text to display on hovered data values
    text = line.mark_text(align="center", dy=-15, fontSize=15, fontWeight="bold",lineBreak = "\n"
                ).encode(text=alt.condition(nearest, 'tool:N', alt.value(' ')))


    # Combine the above into altair plot rules
    rules = (alt.Chart(df)
                .mark_rule(color='gray')
                .encode(x=alt.X("yr:T", axis=alt.Axis(title=None, format=("%Y"), labelAngle=0, tickCount=int(1 + token_A['years'][1] - token_A['years'][0]))))
                .transform_filter(nearest)
                .add_selection(selection)
                .interactive())

    # Create chart layer based on above definitions and rules
    chart = alt.layer(line, selectors, points, rules, text).properties(width=625, height=700)

    return chart
