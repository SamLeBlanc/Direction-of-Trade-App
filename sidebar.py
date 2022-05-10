import streamlit as st

def get_sidebar_selections(data):
    """
    Create the sidebar and collect the user settings needed to make a call to the UN Comtrade API.
    Each subsection below uses selectboxes, multiselects, sliders, etc. to capture the data request
    made by the user. The options are the standard options allowed in the API as described in the
    documentation here: https://comtrade.un.org/data/doc/api
    --------------------------------------------------------------------------------------
    Args:
        data (dict): country and commodity coding data from previously laoded reference data
    Returns:
        token_A (dict): dictionary containing user request information (countries, years, trade direction, etc.)
    """

    # Get lists of names and codes for countries and commodities from previously loaded reference data
    country_names = tuple(data['countries']['country'])
    coded_countries = data['countries']
    coded_products = data['products']

    st.sidebar.title("Direction of Trade App")

    # Each subsection below creates and collects user selections for the API request

    ## Trade Direction (defualt = Export)
    st.sidebar.write('## Trade Direction')
    direction = st.sidebar.selectbox("", ["Export","Import","Net Export"])

    ## Reporting Country (i.e. primary country of interest) (default = USA)
    st.sidebar.write('## Reporting Country')
    reporters = st.sidebar.multiselect('', country_names[1:], ['All'])
    # Convert country name to code (needed for API) using reference data from above
    dat = coded_countries[coded_countries['country'].isin(reporters)]
    reporter_codes = dat.code.values

    ## Partner Country (i.e. secondary country of interest) (default = China)
    st.sidebar.write('## Partner Country')
    partners = st.sidebar.multiselect('', country_names, ['World'])
    # Convert country name to code (needed for API) using reference data from above
    df = coded_countries[coded_countries['country'].isin(partners)]
    parter_codes = df.code.values

    ## Years of interest (for the sake of time, best to select less than 10 years or less)
    st.sidebar.write('## Time Period')
    years = st.sidebar.slider('Note: Selecting >5 years will cause longer load times', 1980, 2020, (1990, 2020))

    ## Trade Commodities
    st.sidebar.write('## Trade Goods')
    ## Commodity Levels
    # Commodity levels refer to the 'size' of the commodity classification. 4-digit classifications are highly specific,
    # 2-digit classifications are groups of 4-digits, and Aggregate is the sum of all commodities of a specific level
    st.sidebar.write('Commodity Levels')
    commodity_levels = st.sidebar.multiselect('', ["Aggregate","2-Digit","4-Digit"], ["Aggregate","2-Digit"])
    cl = {"Aggregate":1, "2-Digit":2, "4-Digit":4}
    # Convert commodity level to integer (needed for API)
    commodity_levels = [cl[l] for l in commodity_levels]

    ## Commodity Codes
    # Get all products in the above selected commodity level
    coded_products = coded_products[coded_products['level'].isin(commodity_levels)]
    # Create dictionary for ids and product names of all products in selected commodity level
    dict = { prod:id for (prod,id) in zip(tuple(coded_products["product"]), tuple(coded_products["id"]))}
    # Create commodity multiselect based on the selected commodity level
    st.sidebar.write('Commodity Codes')
    commodity_codes = st.sidebar.multiselect('Commodity Codes (up to 20)', tuple(coded_products["product"]), ['TOTAL - Total of all HS commodities'])
    # Convert commodities back into commodity codes (needed for API)
    commodity_codes = [dict[code] for code in commodity_codes]

    ## Combine user selections into a dictionary for later use
    token_A = {'reporter_codes' : reporter_codes, 'parter_codes' : parter_codes, 'direction' : direction, 'years' : years, 'commodity_codes' : commodity_codes}
    return token_A
