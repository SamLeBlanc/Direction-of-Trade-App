import streamlit as st

def create_sidebar(data):
    country_names = tuple(data['countries']['country'])
    coded_countries = data['countries']
    coded_products = data['products']

    st.sidebar.write('## 1. Select Trade Direction*')
    direction = st.sidebar.selectbox("", ["Import","Export","re-Import","re-Export","All"])
    tf = {"Import":"1", "Export":"2", "re-Import":"3", "re-Export":"4", "All":"all"}
    direction = tf[direction]

    st.sidebar.write('## 2. Select Reporting Country*')
    reporters = st.sidebar.multiselect('', country_names[1:], ["All"])
    dat = coded_countries[coded_countries['country'].isin(reporters)]
    r_codes = dat.code.values

    st.sidebar.write('## 3. Select Partner Country')
    partners = st.sidebar.multiselect('', country_names, ["World"])
    df = coded_countries[coded_countries['country'].isin(partners)]
    p_codes = df.code.values

    st.sidebar.write('## 4. Select Time Period')
    years = st.sidebar.slider('Note: Selecting more than 10 years will cause longer load times', 1980, 2020, (2010, 2020))

    st.sidebar.write('## 5. Select Goods')
    st.sidebar.write('Commodity Levels')
    commodity_levels = st.sidebar.multiselect('', ["Aggregate","2-Digit","4-Digit"], ["Aggregate","2-Digit"])
    cl = {"Aggregate":1, "2-Digit":2, "4-Digit":4}
    commodity_levels = [cl[l] for l in commodity_levels]
    coded_products = coded_products[coded_products['level'].isin(commodity_levels)]

    ids = tuple(coded_products["id"])
    products = tuple(coded_products["product"])
    dict = { prod:id for (prod,id) in zip(products, ids)}

    st.sidebar.write('Commodity Codes')
    commodity_codes = st.sidebar.multiselect('Commodity Codes (up to 20)', products, ["TOTAL - Total of all HS commodities"])
    commodity_codes = [dict[code] for code in commodity_codes]

    request_dictionary = {"r_codes":r_codes, "p_codes":p_codes, "years":years, "direction":direction, "commodity_codes":commodity_codes}
    return request_dictionary
