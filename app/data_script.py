import requests
import json
import os
import concurrent.futures
import time
from modules.dot_export import secrets

# Declares an absolute path to dotenv file
env_path = os.path.abspath("../.env")
# initiating dot_export module to load .env values
secret_var = secrets(env_path)
# Unpack secrets as a tuple
projected_player_pts, actual_player_pts, team_performance, odds, entry, access = secret_var

filename_mapping = {
    projected_player_pts: "Player_Projection_Stats",
    actual_player_pts: "Player_Actual_Stats",
    team_performance: "Team_Stats",
    odds: "Game_Odds"
}

def get_filename(endpoint):
    return filename_mapping.get(endpoint, "default_filename")

# create function to handle api requests w/ diff yr, wk, and data_types
def data_requests(target_type, target_season, target_week):
    # test_url = f'https://filesamples.com/samples/code/json/sample1.json'

    # declaring url w/ args for versatile api calls
    url = f'{entry}/{target_type}/{target_season}REG/{target_week}?key={access}'

    print(f'  ||  YEAR:{target_season}  ||  WEEK:{target_week} || TARGET: {target_type}  ||')

    target_response = requests.get(url)
    target_data = target_response.json()

    assign_tag = get_filename(target_type)
    tag_name = f'{target_season}_week-{target_week}__{assign_tag}.json'

    with open(f'data_json/{tag_name}', 'w') as json_file:
        json.dump(target_data, json_file)

    with open(f'data_json/{tag_name}', 'r') as json_file:
        loaded_data = json.load(json_file)

    if isinstance(loaded_data, list) and loaded_data:
        fieldnames = loaded_data[0].keys()
        print(fieldnames)
        print("JSON loaded successfully, JSON saved!")
    else:
        print("Data format not recognized.")

    print('FUNCTION ENDED"')


counter = 0
total_requests = 4 * 17 * 4  # 4 endpoints, 17 weeks, 4 years

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

# Using ThreadPoolExecutor for concurrent requests
with concurrent.futures.ThreadPoolExecutor() as executor:
    # Loop through each year, week, and endpoint
    for year in range(2018, 2023):  # From 2019 to 2022
        print(f'||~~~~~~~~~~~~~~~||  WE ARE ON SEASON: { year } ||~~~~~~~~~~~~~~~')

        if year == 2020:
            print(f'||~~~~~~~~~~~~~~~||  WE ARE HALF WAY THERE!!!, {year} ||~~~~~~~~~~~~~~~')

        if year > 2023:
            print(f'||~~~~~~~~~~~~~~~||  WE ARE DONE!!!, {year} ||~~~~~~~~~~~~~~~')

        for week in range(1, 18):  # From week 1 to 17
            print(f'||~~~~~~~~~~~~~~~||  WE ARE ON WEEK: {week}  ||~~~~~~~~~~~~~~~')

            futures = [executor.submit(data_requests, endpoint, year, week) for endpoint in [projected_player_pts, actual_player_pts, team_performance, odds]]
            for future in concurrent.futures.as_completed(futures):
                future.result()
                counter += 1
                print(f"||~~~~~~~~~~~~~~~|| COMPLETED:  {counter}/{total_requests} ||~~~~~~~~~~~~~~~~")
            print(f'||~~~~~~~~~~~~~~~|| NOW WAITING  (60)  SECONDS ||~~~~~~~~~~~~~~~~')
            countdown(60)


