import pandas as pd
import typer
from api_to_dw import get_data, extract_match_data, extract_table_data, extract_scorers_data, to_snake_case
from today_matches import get_today_data, match_data
from send_email import send_email
from common_variable import get_env_variable, load_config


def main():
    config_file = load_config("config.json")
    config_api = config_file["api"]
    config_email = config_file["email"]
    url = config_api["url"]
    league = config_api["league"]
    endpoint_match = config_api["endpoint_match"]
    endpoint_table = config_api["endpoint_table"]
    endpoint_scorers = config_api["endpoint_scorers"]
    drop_columns_today = config_api["drop_columns_today"]
    drop_columns = config_api["drop_columns"]
    password = get_env_variable("PASSWORD")
    api_key = get_env_variable("API_KEY")
    json_response = get_data(url, api_key, endpoint_match, league)
    json_table = get_data(url, api_key, endpoint_table, league)
    json_scorers = get_data(url, api_key, endpoint_scorers, league)
    print(json_response)
    print(json_table)
    print(json_scorers)
    df_match = extract_match_data(json_response, drop_columns)
    df_table =  extract_table_data(json_table)
    df_scorers =  extract_scorers_data(json_scorers)
    df_match.columns = [to_snake_case(col) for col in df_match.columns]
    df_table.columns = [to_snake_case(col) for col in df_table.columns]
    df_scorers.columns = [to_snake_case(col) for col in df_scorers.columns]
    df_scorers = df_scorers.fillna(0)
    df_scorers = df_scorers.astype({col: 'int64' for col in df_scorers.select_dtypes('float64').columns})
    data = get_today_data(config_api, api_key)
    df = match_data(data, drop_columns_today)
    print(df)
    send_email(config_email, password, df)


def run():
    """Main function to run form the command line (entrypoint)"""
    typer.run(main)


if __name__ == "__main__":
    run()
