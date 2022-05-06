import streamlit as st
import pandas as pd
import requests
import numpy as np

def setup_request_A(token):
    """
    The UN Comtrade API is finicky about the max number of a parameters for a given call.
    So, if the class is too large, it is split into several smaller calls.
    """

    # Join reporter, partner, and commodity codes with the url recognized 'space' character ('%2C')
    reporter_codes = '%2C'.join(token['reporter_codes'])
    parter_codes = '%2C'.join(token['parter_codes'])
    commodity_codes = '%2C'.join(token['commodity_codes'])

    # Convert year selections into strings and join sets of five years together
    # Five years is the max number the API will accept, otherwise it must be split into multiple requests
    years_ = [str(i) for i in range(token['years'][0], token['years'][1])]
    years = []
    for i in range(1+len(years_)//5):
        years.append('%2C'.join(years_[i*5 : (i+1)*5]))

    # Create list of calls for the API
    urls = []
    for yr in years:
        url = f"""https://comtrade.un.org/api/get?max=10000&type=C&freq=A&px=HS&ps={yr}&r={reporter_codes}&p={parter_codes}&rg=all&cc={commodity_codes}"""
        urls.append(url)
    return urls

def make_batch_request(urls):
    """
    Make multiple API requests by looping over a list of urls, concating the new
    data each time. The split is usually necessary for calls with a large time range.
    After collecting the data, calculate the net exports and return the dataframe.
    --------------------------------------------------------
    Args:
        urls (list): urls of the API calls to run
    Returns:
        df: concated data from calls with net exports
    """
    df = pd.DataFrame()
    for url in urls:
        df_ = run_single_request(url)
        df = pd.concat([df,df_])
    df = calculate_net_exports(df)
    return df

def run_single_request(url):
    """
    Preforms a single request to the UN Comtrade API and returns the data if the request was successful.
    If the status_code is not 200, then an empty dataframe is returned. However, there can be issues
    even with a 200 code, in such case we print out the validation status for more information.
    ------------------------------------------------------------------
    Args:
        url (string): url request to UN Comtrade API
    Returns:
        df: response data, if the request was successful
    """
    req = requests.get(url)
    # On successful request, convert from JSON and add column headers
    if req.status_code == 200:
        dat = req.json();
        data = dat["dataset"]
        if data:
            df = pd.DataFrame(data[1:], columns = data[0]);
            df = df[['pfCode','yr','rgDesc','rtCode','rtTitle','ptCode','ptTitle','cmdCode','cmdDescE','TradeValue']]
            return df
        # If no data is returned, print the response status
        else:
            print(dat['validation']['status']['name'])
    return pd.DataFrame()



def calculate_net_exports(df):
    """
    Calculate the annual net exports of specific commodity code and country. The API
    only returns imports and exports so the net needs to be calculated seperately. The
    function matches the import and export rows based on other traits, then creates
    a new row in the dataframe for net exports.
    -------------------------------------------------------------
    Args:
        df: annual import and export data by product and country
    Returns:
        df: dataframe with net export rows added
    """
    # Only include standard import and exports (no-import/export)
    df = df.loc[(df.rgDesc == 'Export') | (df.rgDesc == 'Import')]
    df_ = df.copy(deep=True)

    # Iterate over rows matching up import and export rows
    for index, row in df_.iterrows():
        net_exports = np.nan
        counterpart = df_.loc[(df_.yr == row.yr) &
                             (df_.rgDesc != row.rgDesc) &
                             (df_.rtCode == row.rtCode) &
                             (df_.ptCode == row.ptCode) &
                             (df_.cmdCode == row.cmdCode)]

        # Only add the row if the starting row was an export row
        if len(counterpart) == 1 and row.rgDesc == 'Export':
            net_exports = row.TradeValue - counterpart.iloc[0].TradeValue
            new_row = row.to_dict()
            new_row['rgDesc'] = 'Net Export'
            new_row['TradeValue'] = net_exports
            df = df.append(new_row, ignore_index = True)
    return df.reset_index()

def create_commodity_token_B(data, token_A, graphed_countries):
    """
    Create the second call token (token_B) which is gets information about commodity
    goods. token_B is uses several parameters from token_A, with the comoddity codes different.
    ------------------------------------------
    Args:
        data (dict): reference data tables containing coding information
        token_A (dict): request information for the first API call
        graphed_countries (list): list of 10 countries included in the line chart
    Returns:
        token_B (dict): request information for the second API call
    """
    # Convert contry names to codes for API call
    coded_countries = data['countries']
    dat = coded_countries[coded_countries['country'].isin(graphed_countries[0:5])]
    reporter_codes = dat.code.values

    return {'reporter_codes' : reporter_codes,
            'parter_codes' : token_A['parter_codes'],
            'direction' : token_A['direction'],
            'years' : token_A['years'],
            'commodity_codes' : ['AG2']}


def setup_request_B(token_B):
    """
    Convert token_B into an API call by joining several lists with space characters.
    Each dashboard uses two sets of API calls, this formats the second call, which
    returns a list of commodities and trade values for the graphed countries.
    -------------------------------------------------------------
    Args:
        token_B (dict): the user-selected settings necessary for the commodity API call
    Returns:
        urls (list): single element list containing the url string of the API call
    """
    # Join reporter, partner, and commodity codes with the url recognized 'space' character ('%2C')
    reporter_codes = '%2C'.join(token_B['reporter_codes'])
    parter_codes = '%2C'.join(token_B['parter_codes'])
    commodity_codes = '%2C'.join(token_B['commodity_codes'])

    # Use only the most recent year in the dataset
    year = token_B['years'][1]

    # Create API call based on the token_B data
    url = f"""https://comtrade.un.org/api/get?max=10000&type=C&freq=A&px=HS&ps={year}&r={reporter_codes}&p={parter_codes}&rg=all&cc={commodity_codes}"""

    return [url]

def display_API_calls(urls):
    """
    Display a list of all the API calls made for the current settings at the bottom of the page
    ----------------------------------------------------
    Args:
        urls (list): the API calls made for the current settings (created in setup_request_X.py)
    Returns:
        None
    """
    st.write('#### UN Comtrade API Calls:')
    for u in urls: st.write(u)
