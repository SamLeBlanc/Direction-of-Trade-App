import streamlit as st
import numpy as np
import pandas as pd
import requests
import altair as alt

st.title("UN COMTRADE")

coded_countries = pd.read_csv("coded_countries.csv", encoding="ISO-8859-1")
coded_products  = pd.read_csv("coded_products.csv",  encoding="ISO-8859-1")

country_names = tuple(coded_countries.country)

reporters = st.sidebar.multiselect('Reporters (up to 5)', country_names[1:], ["All"])
dat = coded_countries[coded_countries['country'].isin(reporters)]
r_codes = dat.code.values

partners = st.sidebar.multiselect('Partners (up to 5)', country_names, ["World"])
df = coded_countries[coded_countries['country'].isin(partners)]
p_codes = df.code.values

years = st.sidebar.slider('Period', 1980, 2020, (2010, 2020))

direction = st.sidebar.selectbox("Trade Flows", ["Import","Export","re-Import","re-Export","All"])
tf = {"Import":"1", "Export":"2", "re-Import":"3", "re-Export":"4", "All":"all"}
direction = tf[direction]

commodity_levels = st.sidebar.multiselect('Commodity Levels', ["Aggregate","2-Digit","4-Digit"], ["Aggregate","2-Digit"])
cl = {"Aggregate":1, "2-Digit":2, "4-Digit":4}
commodity_levels = [cl[l] for l in commodity_levels]
coded_products = coded_products[coded_products['level'].isin(commodity_levels)]

ids = tuple(coded_products["id"])
products = tuple(coded_products["product"])
dict = { prod:id for (prod,id) in zip(products, ids)}

commodity_codes = st.sidebar.multiselect('Commodity Codes (up to 20)', products, ["TOTAL - Total of all HS commodities"])
commodity_codes = [dict[code] for code in commodity_codes]

request_dictionary = {"r_codes":r_codes, "p_codes":p_codes, "years":years, "direction":direction, "commodity_codes":commodity_codes}

df = pd.read_pickle("hold.pkl")

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

def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '$%.1f%s' % (num, ['', 'K', 'M', 'B', 'T', 'P'][magnitude])

# df.to_pickle("hold.pkl")

df2 = df.groupby('rtTitle').sum()
df2 = df2[['TradeValue']].sort_values(by="TradeValue", ascending=False)
df2 = df2.iloc[0:10,:].reset_index()

df = df[df['rtTitle'].isin(list(df2.rtTitle))]
df['yr'] = pd.to_datetime(df['yr'], format="%Y")
df['tool'] = df['TradeValue'].apply(lambda row: human_format(row))

nearest = alt.selection(type='single', nearest=True, on='mouseover', fields=['yr'], empty='none')

line = alt.Chart(df).mark_line().encode(x='yr:T', y='TradeValue:Q', color='rtTitle:N')

selectors = alt.Chart(df).mark_point().encode(x='yr:T', opacity=alt.value(0)).add_selection(nearest)

points = line.mark_point().encode(opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

text = line.mark_text(align="center", dy=-15, fontSize=15, fontWeight="bold",lineBreak = "\n"
            ).encode(text=alt.condition(nearest, 'tool:N', alt.value(' ')))

selection = alt.selection_multi(fields=['rtTitle'], bind='legend')

y = [int(i) for i in years]
y_ = 1 + max(y) - min(y)

rules = (alt.Chart(df)
            .mark_rule(color='gray')
            .encode(x=alt.X("yr:T", axis=alt.Axis(title=None, format=("%Y"), labelAngle=0, tickCount=int(y_))))
            .transform_filter(nearest)
            .add_selection(selection)
            .interactive())

chart = alt.layer(line, selectors, points, rules, text).properties(width=800, height=600)
chart

if st.button('Show API Call'):
     for u in urls:
         st.write(u)
else:
     pass
