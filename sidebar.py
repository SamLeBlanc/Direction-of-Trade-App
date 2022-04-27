import streamlit as st

def create_sidebar(data):

    st.sidebar.title("Direction of Trade App")

    country_names = tuple(data['countries']['country'])
    coded_countries = data['countries']
    coded_products = data['products']

    st.sidebar.write('## Trade Direction')
    direction = st.sidebar.selectbox("", ["Import","Export","Net Export"])

    st.sidebar.write('## Reporting Country')
    reporters = st.sidebar.multiselect('', country_names[1:], ['All'])
    dat = coded_countries[coded_countries['country'].isin(reporters)]
    reporter_codes = dat.code.values

    st.sidebar.write('## Partner Country')
    partners = st.sidebar.multiselect('', country_names, ['World'])
    df = coded_countries[coded_countries['country'].isin(partners)]
    parter_codes = df.code.values

    st.sidebar.write('## Time Period')
    years = st.sidebar.slider('Note: Selecting >5 years will cause longer load times', 1980, 2020, (2010, 2020))

    st.sidebar.write('## Goods')
    st.sidebar.write('Commodity Levels')
    commodity_levels = st.sidebar.multiselect('', ["Aggregate","2-Digit","4-Digit"], ["Aggregate","2-Digit"])
    cl = {"Aggregate":1, "2-Digit":2, "4-Digit":4}
    commodity_levels = [cl[l] for l in commodity_levels]
    coded_products = coded_products[coded_products['level'].isin(commodity_levels)]

    ids = tuple(coded_products["id"])
    products = tuple(coded_products["product"])
    dict = { prod:id for (prod,id) in zip(products, ids)}

    st.sidebar.write('Commodity Codes')
    commodity_codes = st.sidebar.multiselect('Commodity Codes (up to 20)', products, ['TOTAL - Total of all HS commodities'])
    commodity_codes = [dict[code] for code in commodity_codes]

    return {
        'reporter_codes' : reporter_codes,
        'parter_codes' : parter_codes,
        'direction' : direction,
        'years' : years,
        'commodity_codes' : commodity_codes
    }
