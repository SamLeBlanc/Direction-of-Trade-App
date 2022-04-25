import pandas as pd
import altair as alt

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '$%.1f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

def calculate_net_exports(df):
    df = df.loc[(df.rgDesc == 'Export') | (df.rgDesc == 'Import')]
    df_ = df.copy(deep=True)
    for index, row in df_.iterrows():
        net_exports = np.nan
        counterpart = df_.loc[(df_.yr == row.yr) &
                             (df_.rgDesc != row.rgDesc) &
                             (df_.rtCode == row.rtCode) &
                             (df_.ptCode == row.ptCode) &
                             (df_.cmdCode == row.cmdCode)]

        if len(counterpart) == 1 and row.rgDesc == 'Export':
            net_exports = row.TradeValue - counterpart.iloc[0].TradeValue
            new_row = row.to_dict()
            new_row['rgDesc'] = 'Net Export'
            new_row['TradeValue'] = net_exports
            df = df.append(new_row, ignore_index = True)
    return df.reset_index()

def create_chart(df, request_dictionary):

    tf = {"1":"Import", "2":"Export", "all":"Net Export"}
    direction = tf[request_dictionary['direction']]

    df = df[df.rgDesc == direction]

    df2 = df[df.yr == max(df.yr)]
    df2 = df2.sort_values(by="TradeValue", ascending=False)
    if direction in ['Import','Export']:
        df2 = df2.iloc[0:10,:].reset_index()
    else:
        df2 = pd.concat([df2.iloc[0:5,:], df2.iloc[-5:,:]]).reset_index()

    top_cont = list(df2.rtTitle)

    df = df[df['rtTitle'].isin(list(df2.rtTitle))]
    df['yr'] = pd.to_datetime(df['yr'], format="%Y")
    df['tool'] = df['TradeValue'].apply(lambda row: human_format(row))

    nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['yr'], empty='none')

    line = alt.Chart(df).mark_line().encode(x='yr:T', y='TradeValue:Q',
        color = alt.Color('rtTitle:N', sort=alt.EncodingSortField('TradeValue', op='mean', order='descending')))

    selectors = alt.Chart(df).mark_point().encode(x='yr:T', opacity=alt.value(0)).add_selection(nearest)

    points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

    text = line.mark_text(align="center", dy=-15, fontSize=15, fontWeight="bold",lineBreak = "\n"
                ).encode(text=alt.condition(nearest, 'tool:N', alt.value(' ')))

    selection = alt.selection_multi(fields=['rtTitle'], bind='legend')

    y = [int(i) for i in range(2010,2020)]
    y_ = 1 + max(y) - min(y)

    rules = (alt.Chart(df)
                .mark_rule(color='gray')
                .encode(x=alt.X("yr:T", axis=alt.Axis(title=None, format=("%Y"), labelAngle=0, tickCount=int(y_))))
                .transform_filter(nearest)
                .add_selection(selection)
                .interactive())

    chart = alt.layer(line, selectors, points, rules, text).properties(width=600, height=600)
    return chart, top_cont
