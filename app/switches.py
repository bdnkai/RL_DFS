import os
import json
import pandas as pd
from pandas import json_normalize


data_types = ['Player_Projection_Stats', 'Player_Actual_Stats', 'Team_Stats', 'Game_Odds']

def dispatch_converter(raw_data, json_file_path, csv_file_path):
    match raw_data:
        case 'Sports_Book':
            print('~~ SWITCH ACTIVATED FOR ||  Game_Odds  ||')
            raw_csv_path = csv_file_path
            raw_json_path = json_file_path

            with open(raw_json_path, 'r') as f:
                raw_json_data = json.load(f)

            raw_csv_data = json_normalize(raw_json_data)
            raw_csv_data.to_csv(raw_csv_path, index=False)
            return

        case 'Sports_Data':
            print(f'SWITCH ACTIVATED FOR ||  {csv_file_path}  ||')
            raw_csv_path = csv_file_path
            raw_json_path = json_file_path

            with open(raw_json_path, 'r') as f:
                raw_json_data = json.load(f)

            raw_csv_data = pd.DataFrame(raw_json_data)
            raw_csv_data.to_csv(raw_csv_path, index=False)
            raw_csv_data.head(), raw_csv_path
            return


def dispatch_cleaner(raw_data, target_type, target_season, target_week):
    match raw_data:
        case 'empty_cells':

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

            if target_type == "Player_Projection":
                dispatch_cleaner("player_projection", target_type=target_type, target_season=target_season, target_week=target_week)

        case 'player_projection':

            print(f' {target_season} | {target_week} | {target_type} ')
            tag_name = f'{target_season}_week-{target_week}__{target_type}'
            print(tag_name)

            csv_file_path = f'../data_csv/{tag_name}.csv'

            post_process_path = f'../data_RL/{tag_name}.csv'

            clean_file_csv = pd.read_csv(csv_file_path)

            cleaned_v2 = clean_file_csv.loc[:, ~clean_file_csv.columns.str.contains('Scrambled')]
            important_cols = ['PlayerID', 'Season', 'GameDate', 'Week', 'Team', 'Opponent', 'HomeOrAway', 'Number',
                              'Name']

            cols_to_remove = []
            for col in cleaned_v2.columns:
                if col not in important_cols:
                    if cleaned_v2[col].duplicated(keep=False).all():
                        cols_to_remove.append(col)
            print(f'{cols_to_remove}')
            cleaned_v2.drop(columns=cols_to_remove, inplace=True)
            cleaned_v2.to_csv(post_process_path, index=False)

            return
        case 'Player_Actual_Stats':
            raw_csv_path = csv_file_path
            raw_json_path = json_file_path

            return
        case 'Team_Stats':
            raw_csv_path = csv_file_path
            raw_json_path = json_file_path


            return