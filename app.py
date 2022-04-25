import pandas as pd
import numpy as np

from st_btn_select import st_btn_select

from sidebar import *
from setup import *
from charts import *
from calls import *

def top_goods(df):
    # df_ = df.loc[(df['rtTitle'] == 'USA') & (df['ptTitle'] == 'China')
    return ""

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

def main():
    alter_default_CSS()
    data = load_reference_tables()
    request_dictionary = create_sidebar(data)
    urls = setup_api_request(request_dictionary)

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

    df = pd.read_pickle("hold.pkl")
    # st.write(df)

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
