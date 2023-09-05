import requests
import csv
import json
import os
from modules.dot_export import secrets

# Declares an absolute path to dotenv file
env_path = os.path.abspath("../.env")
# initiating dot_export module to load .env values
secret_var = secrets(env_path)
# Unpack secrets as a tuple
projected_player_pts, actual_player_pts, team_performance, odds, entry, access = secret_var
# print(secret_var)
season, week = 2019, 1

filename_mapping = {
    projected_player_pts: "Player_Projection_Stats",
    actual_player_pts: "Player_Actual_Stats",
    team_performance: "Team_Stats",
    odds: "Game_Odds"

}

def get_filename(endpoint):
    return filename_mapping.get(endpoint, "default_filename")

# create function to handle apu requests w/ diff yr, wk, and data_types
def data_requests(target_type, target_season, target_week):
    # declaring url w/ args for versatile api calls
    url = f'https://filesamples.com/samples/code/json/sample1.json'

    # url = f'{entry}/{target_type}/{target_season}REG/{target_week}?key={access}'
    print(f'Data_Type:{target_type},  Uear:{target_season},  WEEK:{target_week}')

    target_response = requests.get(url)
    target_data = target_response.json()

    assign_tag = get_filename(target_type)
    print(assign_tag)

    tag_name = f'{target_season}_week-{target_week}__{assign_tag}.json'
    print(tag_name)

    with open(f'data_json/{tag_name}', 'w') as json_file:
        json.dump(f'{target_data}', json_file)

    with open(f'data_json/{tag_name}', 'r') as json_file:
        loaded_data = json.load(json_file)

    if isinstance(loaded_data, list) and loaded_data:
        fieldnames = loaded_data[0].keys()
        print(fieldnames)
        print(loaded_data)

    else:
        print("Data format not recognized.")


data_requests(projected_player_pts, season, week)
#
# data_type = "2019REG/1?key="
#
#

# print("CSV conversion completed and saved to 'S_2020_G_1.csv'")