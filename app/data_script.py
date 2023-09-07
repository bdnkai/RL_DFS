import requests
import json
import os
import concurrent.futures
import time
from modules.dot_export import secrets

#
env_path = os.path.abspath("../.env")
secret_var = secrets(env_path)
projected_player_pts, actual_player_pts, team_performance, odds, entry, access = secret_var

filename_mapping = {
    projected_player_pts: "Player_Projection_Stats",
    actual_player_pts: "Player_Actual_Stats",
    team_performance: "Team_Stats",
    odds: "Game_Odds"
}

def get_filename(endpoint):
    return filename_mapping.get(endpoint, "default_filename")

def data_requests(target_type, target_season, target_week):
    # declaring url w/ args for versatile api calls
    # url = f'https://filesamples.com/samples/code/json/sample1.json'

    url = f'{entry}/{target_type}/{target_season}REG/{target_week}?key={access}'
    print(f'  ||  YEAR:{target_season}  ||  WEEK:{target_week} || TARGET: {target_type}  ||')

    try:
        target_response = requests.get(url)
        target_data = target_response.json()
        # print(target_data)
        assign_tag = get_filename(target_type)
        tag_name = f'{target_season}_week-{target_week}__{assign_tag}.json'
        # print(tag_name)

        if tag_name and target_data:
            print(tag_name)
            print(target_data)

            try:
                with open(f'test/{tag_name}', 'w') as json_file:
                    json.dump(target_data, json_file)

                with open(f'test/{tag_name}', 'r') as json_file:
                    loaded_data = json.load(json_file)
                    print(loaded_data)

                if isinstance(loaded_data, list) and loaded_data:
                    fieldnames = loaded_data[0].keys()
                    print(fieldnames)
                    print("JSON loaded successfully, JSON saved!")
                else:
                    print("Data format not recognized.")

            except:
                print('no json file, unable to save or read')
    except:
        pass
        print(f'invalid api URL, please check if the URL is valid')


counter = 0
access_points =  4
weeks_per_season = 18
season_interest_start = 2012
season_interest_end = 2022
total_seasons = season_interest_end - season_interest_start
total_requests = access_points * weeks_per_season * total_seasons

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='/r')
        time.sleep(1)
        t -= 1


with concurrent.futures.ThreadPoolExecutor() as executor:
    for year in range(2017, 2018):
        print(f'||  WE ARE ON SEASON: { year } ')

        if year > 2011:
            set_range = range(1,18)
        else:
            set_range = range(1,18)

        for week in set_range:
            print(f' WE ARE ON WEEK: {week}  ')
            futures = [executor.submit(data_requests, endpoint, year, week) for endpoint in [projected_player_pts, actual_player_pts, team_performance, odds]]
            for future in concurrent.futures.as_completed(futures):
                future.result()
                counter += 1
                print(f"COMPLETED:  {counter}/{total_requests}")
            print(f'NOW WAITING  (60)  SECONDS')
            countdown(8)


