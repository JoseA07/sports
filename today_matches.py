import pandas as pd
import requests


def get_today_data(config:str, api_key:str) -> dict:
    """
    Get data from an API:
    - get the datafrom football api

    Parameters:
    - url (str): api url
    - endpoint: endpoint for the api
    - league (str): league code
    - headers (dict): adict with params for the dict

    Returns:
    - pd.DataFrame: JSON with the api response
    """
    full_url = f'{config["url_today_match"]}'
    headers = {"X-Auth-Token": api_key}
    response = requests.get(full_url, headers=headers)
    data = response.json()
    return data


def match_data(response: dict, drop_columns: list) -> pd.DataFrame:
    """
    Extract match data:
    - Extract the match data from the json result from football api

    Parameters:
    - response (dict): api response

    Returns:
    - pd.DataFrame: DataFrame football match data
    
    """
    df = pd.json_normalize(response['matches'])
    valid_drop = [col for col in drop_columns if col in df.columns]
    print("Dropping:", valid_drop)
    df = df.drop(columns=valid_drop)
    return df
