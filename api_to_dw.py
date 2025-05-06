import pandas as pd
import requests
import re

pd.set_option('display.max_columns', None)


def get_data(url:str, api_key:str, endpoint:str, league:str) -> dict:
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
    full_url = f'{url}/{league}/{endpoint}'
    headers = {"X-Auth-Token": api_key}
    response = requests.get(full_url, headers=headers)
    data = response.json()
    return data


def extract_match_data(response: dict, drop_columns: list) -> pd.DataFrame:
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


def extract_table_data(response: dict) -> pd.DataFrame:
    """
    Extract position table data:
    - Extract the position table data from the json result from football api

    Parameters:
    - response (dict): api response

    Returns:
    - pd.DataFrame: DataFrame football position table data
    
    """
    df = pd.json_normalize(response['standings'][0]['table'])
    return df


def extract_scorers_data(response: dict) -> pd.DataFrame:
    """
    Extract scorers data:
    - Extract the scorers data from the json result from football api

    Parameters:
    - response (dict): api response

    Returns:
    - pd.DataFrame: DataFrame football scorers data
    
    """
    df = pd.json_normalize(response["scorers"])
    return df


def to_snake_case(name):
    """
    Convert to snake case column name
    """
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("__([A-Z])", r"_\1", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name)
    name = name.replace('.', '_')                         
    name = name.replace(' ', '_') 
    return name.lower()
