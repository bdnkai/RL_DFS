import os
import json
import concurrent.futures
import pandas as pd



data_types = ['Player_Projection_Stats', 'Player_Actual_Stats', 'Team_Stats', 'Game_Odds']

total_data_type = len(data_types)
weeks_per_season = 18
season_interest_start = 2012
season_interest_end = 2023
total_seasons = season_interest_end - season_interest_start
total_request = total_data_type * total_seasons * weeks_per_season


def data_filter2(clean_file_path, tag_name):

    file_path = clean_file_path
    post_process_path = f'../data_finalized/{tag_name}v2.csv'
    clean_file_csv = pd.read_csv(file_path)

    cleaned_v2 = clean_file_csv.loc[:, ~clean_file_csv.columns.str.contains('Scrambled')]
    important_cols = ['PlayerID', 'Season', 'GameDate', 'Week', 'Team', 'Opponent', 'HomeOrAway', 'Number', 'Name']

    cols_to_remove = []
    for col in cleaned_v2.columns:
        if col not in important_cols:
            if cleaned_v2[col].duplicated(keep=False).all():
                cols_to_remove.append(col)
    print(f'{cols_to_remove}')
    cleaned_v2.drop(columns=cols_to_remove, inplace=True)

    # cleaned_file_path_v3 = file_path
    cleaned_v2.to_csv(post_process_path, index=False)

def data_filter(target_type, target_season, target_week):
    print(target_type)

    print(f' {target_season} | {target_week} | {target_type} ')
    tag_name = f'{target_season}_week-{target_week}__{target_type}'
    print(tag_name)

    csv_file_path = f'../data_csv/{tag_name}.csv'
    post_process_path = f'../data_RL/{tag_name}.csv'

    print(post_process_path)

    clean_file_csv = pd.read_csv(csv_file_path)
    columns_to_remove = []

    for col in clean_file_csv.columns:
        if pd.api.types.is_numeric_dtype(clean_file_csv[col]):
            unique_values = clean_file_csv[col].dropna().unique()
            if all(0 <= val <= 1 for val in unique_values):
                columns_to_remove.append(col)

        columns_to_remove += [col for col in clean_file_csv.columns if 'Scrambled' in col]

        cleaned_v1 = clean_file_csv.drop(columns=columns_to_remove)

        cleaned_csv_path = post_process_path
        cleaned_v1.to_csv(post_process_path, index=False)

        cleaned_csv_path, len(columns_to_remove)

        data_filter2(post_process_path, tag_name)


data_filter(data_types[0],season_interest_end-1, 17)


# with concurrent.futures.ThreadPoolExecutor() as executor:
#     for year in range(season_interest_start, season_interest_end):
#         if year > season_interest_start:
#             set_range = range(1, 18)
#         else:
#             set_range = range(1, 18)
#         for week in set_range:
#             futures = [executor.submit(data_filter,endpoint, year, week) for endpoint in data_types]
#             for future in concurrent.futures.as_completed(futures):
#                 future.result()
