import streamlit as st
import pandas as pd
import requests

def show_api_call_button(urls):
    if st.button('Show API Call'):
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

def setup_api_request(request_dictionary):
    r_codes = '%2C'.join(request_dictionary['r_codes'])
    p_codes = '%2C'.join(request_dictionary['p_codes'])
    direction = request_dictionary['direction']
    commodity_codes = '%2C'.join(request_dictionary['commodity_codes'])
    years = [str(i) for i in range(request_dictionary['years'][0], request_dictionary['years'][1])]
    years_ = []
    for i in range(len(years)//5):
        years_.append('%2C'.join(years[i*5 : (i+1)*5]))

    # df = pd.DataFrame()
    urls = []
    for yr in years_:
        url = f"""https://comtrade.un.org/api/get?max=10000&type=C&freq=A&px=HS&ps={yr}&r={r_codes}&p={p_codes}&rg={direction}&cc={commodity_codes}"""
        urls.append(url)
        # df_ = run_api_request(url)
        # df = pd.concat([df,df_])

    # df.to_pickle("hold.pkl")
    return urls
