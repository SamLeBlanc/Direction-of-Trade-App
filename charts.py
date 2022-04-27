import pandas as pd
import altair as alt
import numpy as np

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


def create_chart(df, token):
    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['yr'], empty='none')

    line = alt.Chart(df).mark_line().encode(x='yr:T', y='TradeValue:Q',
        color = alt.Color('rtTitle:N', sort=alt.EncodingSortField('TradeValue', op='mean', order='descending')))

    selectors = alt.Chart(df).mark_point().encode(x='yr:T', opacity=alt.value(0)).add_selection(nearest)

    points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

    text = line.mark_text(align="center", dy=-15, fontSize=15, fontWeight="bold",lineBreak = "\n"
                ).encode(text=alt.condition(nearest, 'tool:N', alt.value(' ')))

    selection = alt.selection_multi(fields=['rtTitle'], bind='legend')

    rules = (alt.Chart(df)
                .mark_rule(color='gray')
                .encode(x=alt.X("yr:T", axis=alt.Axis(title=None, format=("%Y"), labelAngle=0, tickCount=int(1 + token['years'][1] - token['years'][0]))))
                .transform_filter(nearest)
                .add_selection(selection)
                .interactive())

    chart = alt.layer(line, selectors, points, rules, text).properties(width=625, height=700)
    return chart
