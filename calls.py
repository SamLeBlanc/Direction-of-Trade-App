import streamlit as st
import pandas as pd
import requests
import numpy as np

def show_api_call_button(urls):
    if st.button('Show API Call'):
        token['reporters'] = 'China'
        redraw(data, token)
        for u in urls:
             st.write(u)
    else:
         pass

def run_api_request(url):
    req = requests.get(url)
    if req.status_code == 200:
        dat = req.json();
        data = dat["dataset"]
        if data:
            df = pd.DataFrame(data[1:], columns = data[0]);
            df = df[['pfCode','yr','rgDesc','rtCode','rtTitle','ptCode','ptTitle','cmdCode','cmdDescE','TradeValue']]
            return df
        else:
            print(dat['validation']['status']['name'])
    return pd.DataFrame()

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

def setup_api_request(token):
    r_codes = '%2C'.join(token['r_codes'])
    p_codes = '%2C'.join(token['p_codes'])
    direction = token['direction']
    commodity_codes = '%2C'.join(token['commodity_codes'])
    years = [str(i) for i in range(token['years'][0], token['years'][1])]
    years_ = []
    for i in range(len(years)//5):
        years_.append('%2C'.join(years[i*5 : (i+1)*5]))

    df = pd.DataFrame()
    urls = []
    for yr in years_:
        url = f"""https://comtrade.un.org/api/get?max=10000&type=C&freq=A&px=HS&ps={yr}&r={r_codes}&p={p_codes}&rg=All&cc={commodity_codes}"""
        urls.append(url)
    #     df_ = run_api_request(url)
    #     df = pd.concat([df,df_])
    #
    # df = calculate_net_exports(df)
    # df.to_pickle("hold1.pkl")
    return urls

def get_commodity_data(token):
    r_codes = '%2C'.join(token['r_codes'])
    p_codes = '%2C'.join(token['p_codes'])
    direction = token['direction']
    commodity_codes = 'AG2'
    yr = token['years'][1]
    df = pd.DataFrame()
    urls = []
    url = f"""https://comtrade.un.org/api/get?max=10000&type=C&freq=A&px=HS&ps={yr}&r={r_codes}&p={p_codes}&rg=All&cc={commodity_codes}"""
    urls.append(url)
    # df = run_api_request(url)
    # df = calculate_net_exports(df)
    # df.to_pickle("hold2.pkl")
    return df
