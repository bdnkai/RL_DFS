
import os
import json
import pandas as pd
from pandas import json_normalize








CSV_PATH_DIR = os.path.abspath(path='../data/CSV_DIR')
JSON_DIR_PATH =  os.path.abspath(path='../data/JSON_DIR')
# JSON_SPLIT_DIR = os.path.abspath(path=f'{JSON_DIR_PATH}/SPLIT\\')
# JSON_MERGE_DIR = os.path.abspath(path=f'{JSON_DIR_PATH}/MERGE\\')
#
#
# PREP_FILE_DIR = os.path.abspath(path=f'{CSV_PATH_DIR}\\PREPARE\\')
# CLEAN_FILE_DIR = os.path.abspath(path=f'{CSV_PATH_DIR}\\CLEAN\\')
# MERGE_FILE_DIR = os.path.abspath(path=f'{CSV_PATH_DIR}\\MERGE\\')
# FINAL_FILE_DIR = os.path.abspath(path=f'{CSV_PATH_DIR}\\FINAL\\')
# # folder_types = [JSON_DIR_PATH, CSV_PATH_DIR, CLEAN_FILE_DIR, PREP_FILE_DIR, MERGE_FILE_DIR, FINAL_FILE_DIR, JSON_SPLIT_DIR, JSON_MERGE_DIR]

# Create directories if they don't exist
# directory_list = [JSON_DIR_PATH,JSON_SPLIT_DIR,JSON_MERGE_DIR,CSV_PATH_DIR,CLEAN_FILE_DIR, FINAL_FILE_DIR]

# for directory in directory_list:
#     if not os.path.exists(directory):
#         os.makedirs(directory)

# Move the uploaded JSON files to the 'data_json' directory
json_files = [
    f'{JSON_DIR_PATH}\\2022_week-17__Team_Stats.json',
    f'{JSON_DIR_PATH}\\2022_week-17__Player_Projection_Stats.json',
    f'{JSON_DIR_PATH}\\2022_week-17__Player_Actual_Stats.json',
    f'{JSON_DIR_PATH}\\2022_week-17__Game_Odds.json'
]
for json_file in json_files:
    os.path.abspath(JSON_DIR_PATH)

# Load Game_Odds.json and split the truncated 'PregameOdds' dictionaries
with open(f'../data/JSON_DIR/2022_week-16__Game_Odds.json', 'r') as f:
    game_odds_data = json.load(f)

# Initialize a list to hold the new dictionaries (from splitting 'PregameOdds')
new_dicts = []
for item in game_odds_data:
    if 'PregameOdds' in item:
        for sub_item in item['PregameOdds']:
            new_dict = sub_item.copy()
            new_dict.update({k: item[k] for k in item if k != 'PregameOdds'})
            new_dicts.append(new_dict)

# Save each new dictionary to a separate JSON file in 'OUT' directory
for i, new_dict in enumerate(new_dicts):
    with open(f'{JSON_MERGE_DIR}\\split_{i}.json', 'w') as f:
        json.dump(new_dict, f)

# Convert the new dictionaries to a DataFrame, take average on 'ScoreId'
df_game_odds_split = pd.DataFrame(new_dicts)
df_game_odds_avg = df_game_odds_split.groupby('ScoreId').mean().reset_index()

# Convert the original Game_Odds data to a DataFrame and merge
df_game_odds_original = pd.DataFrame(game_odds_data)
df_game_odds_final = pd.merge(df_game_odds_original, df_game_odds_avg, on='ScoreId', how='left')

# Save the final DataFrame to CSV in 'data_csv' directory
df_game_odds_final.to_csv('data_csv/2022_week-16__Game_Odds.csv', index=False)

# Load Player_Actual_Stats.json and Player_Projection_Stats.json
with open('../data/JSON_DIR/2022_week-16__Player_Actual_Stats.json', 'r') as f:
    player_actual_data = json.load(f)
with open('../data/JSON_DIR/2022_week-16__Player_Projection_Stats.json', 'r') as f:
    player_projection_data = json.load(f)

# Convert to DataFrames
df_player_actual = pd.DataFrame(player_actual_data)
df_player_projection = pd.DataFrame(player_projection_data)

# Add prefixes to column names
df_player_actual = df_player_actual.add_prefix('actual_')
df_player_projection = df_player_projection.add_prefix('projected_')

# Merge the two DataFrames side by side
df_player_merged = pd.concat([df_player_actual, df_player_projection], axis=1)

# Remove any columns that have all NaN values
nan_columns = df_player_merged.columns[df_player_merged.isna().all()].tolist()
df_player_merged.drop(columns=nan_columns, inplace=True)

# Save the merged DataFrame to CSV in 'data_csv' directory
df_player_merged.to_csv('data_csv/2022_week-16__Player_Merged.csv', index=False)

# Load Team_Stats.json
with open(f'{JSON_DIR_PATH}/2022_week-16__Team_Stats.json', 'r') as f:
    team_stats_data = json.load(f)

# Convert to DataFrame
df_team_stats = pd.DataFrame(team_stats_data)

# Merge all the CSVs together
df_final_merge = pd.merge(df_game_odds_final, df_player_merged, left_on='ScoreId', right_on='actual_ScoreId', how='left')
df_final_merge = pd.merge(df_final_merge, df_team_stats, left_on='ScoreId', right_on='ScoreId', how='left')

# Drop specified columns
columns_to_drop = ['HomeRotationNumber', 'AwayRotationNumber', 'LiveOdds', 'Status', 'AwayTeamId', 'HomeTeamId',
                   'GlobalAwayTeamId', 'GlobalHomeTeamId', 'ScoreId']
df_final_merge.drop(columnsf=columns_to_drop, inplace=True)

# Save the final merged DataFrame to CSV in 'data_csv' directory
df_final_merge.to_csv('data_csvf/{JSON_DIR_PATH}/2022_week-16__Final_Merged.csv', index=False)


jobs =  'PREP', 'CLEAN', 'MERGE', 'FINAL', 'SPLIT'
data_types = 'Player_Projection_Stats', 'Player_Actual_Stats', 'Team_Stats', 'Game_Odds'
specifier = 'JSON', 'CSV'


for folder in folder_types:
    os.makedirs(folder, exist_ok=True)
