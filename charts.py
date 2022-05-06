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
        num (float): number to be converted to short scientific format
    Returns:
        num (string): formatted number
    """
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '$%.1f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def create_commodity_list_B(df):
    """
    Creates the list of top commodities displayed in the right column. Trade values
    of different commodities are aggregated amount amoung all of the graphed countries
    for only the most recent year in the dataset. The list is created with HTML
    and set using the streamlit markdown command
    ----------------------------------------------------------------
    Args:
        df (df): dataframe containing the commodity trade values for all graphed countries
    Returns:
        None
    """
    # Limit data to only the most recent year in dataset
    df = df[df.yr == max(df.yr)]

    # Group data by commodity name and summarize with summation
    df = df.groupby(by=["cmdDescE"]).sum().reset_index()

    # Select only commodity name and TradeValue columns, and sort by TradeValue
    df = df[['cmdDescE','TradeValue']].sort_values(by='TradeValue', ascending=False)

    # Reformat TradeValue into a string with comma seperators
    df['TradeValue'] = df.apply(lambda x: "{:,}".format(x['TradeValue']), axis=1)

    # Create list of the top 10 commodities in the grouped dataset
    commodity_list = ''
    for index, row in df[:10].iterrows():
        commodity_list += f'''
        <span style="font-family:sans-serif; color:Green; font-size: 22px; font-weight: 900;">${row.TradeValue}</span>
        <span style="color:#0E1117">-</span>
        <span style="font-family:sans-serif; color:White; font-size: 16px;">{row.cmdDescE}</span>\n
        '''

    # Display the list with markdown format
    st.markdown(commodity_list, unsafe_allow_html=True)

def format_linechart_data(df, token_A):
    """
    Convert data from the API request into a graphable format. Most of this function
    is choosing and subsetting the countries to include in the plot (too many and it
    looks cluttered). Also formats the tooltip and axis labels.
    ------------------------------------------------------------------
    Args:
        df (df): data returned from API request in base format
        token_A (dict):  dictionary containing user request information (countries, years, trade direction, etc.)
    Returns:
        df (df): reformatted dataframe, ready to be plotted
        graphed_countries (list): the 10 countries to be included in the line chart
    """
    # Include data for only the user selected trade direction
    df = df[df.rgDesc == token_A['direction']]

    # With more than 10 countries, the line chart becomes very cluttered
    # The code below selects the 10 countries that will appear on the graph
    # For imports and exports, the graph displays the countries with the highest
    # totals in the most recent year being graphed. For net exports, the graph shows
    # the five most positive and five most negative net exporters.

    # Create new dataframe to find which countries will be graphed
    # Limit data to only the most recent year being graphed
    df_plot = df[df.yr == max(df.yr)]

    # Sort by TradeValue (amount of trading in $$)
    df_plot = df_plot.sort_values(by="TradeValue", ascending=False)

    # If the trade direction of interest is import or export, keep only the top 10 countries
    if token_A['direction'] in ['Import','Export']:
        df_plot = df_plot.iloc[0:10,:].reset_index()
    # If the trade direction of interest is net exports, keep the top and bottom 5 countries
    else:
        df_plot = pd.concat([df_plot.iloc[0:5,:], df_plot.iloc[-5:,:]]).reset_index()

    # Get list of countries in the dataframe (these are the countries that will be graphed)
    graphed_countries = list(df_plot.rtTitle)

    # Subset original dataframe to only include those countries being graphed
    df = df[df['rtTitle'].isin(graphed_countries)]

    # Format y-axis values (year)
    df['yr'] = pd.to_datetime(df['yr'], format="%Y")

    # Create tooltip column to display text on chart hover
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
    Returns:
        chart (altair chart): annual linechart of trade values by country
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
