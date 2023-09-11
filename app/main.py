import os
import pandas as pd
import concurrent.futures
from scripts.json_to_csv import data_conversion
from switches import dispatch_converter, dispatch_cleaner

if __name__ == '__main__':

    data_types = ['Player_Projection_Stats', 'Player_Actual_Stats', 'Team_Stats', 'Game_Odds']

    total_data_type = len(data_types)
    weeks_per_season = 18
    season_interest_start = 2012
    season_interest_end = 2023
    total_seasons = season_interest_end - season_interest_start
    total_request = total_data_type * total_seasons * weeks_per_season
    # abs_path = dir_path = os.path.abspath("/rl_dfs/")





    with concurrent.futures.ThreadPoolExecutor() as executor:
        for year in range(season_interest_start, season_interest_end):
            if year > 2012:
                set_range = range(1, 18)
            else:
                set_range = range(1, 18)

            for week in set_range:

                futures = [executor.submit(data_conversion, endpoint, year, week) for endpoint in data_types]
                print(data_types)

                for future in concurrent.futures.as_completed(futures):
                    future.result()
