# Importing required libraries
import json
import pandas as pd



# Load the JSON file to inspect its structure
file_path = 'X:/Personal_Project/bdn_portfolio/rl_dfs/app/data/JSON_DIR/2022_week-17__Game_Odds.json'
with open(file_path, 'r') as f:
    game_odds_data = json.load(f)

# Display the first few records to understand the data structure
# sample_data = {k: game_odds_data[k] for k in list(game_odds_data.keys())[:2]}
# print(sample_data)
# Initialize an empty list to store the flattened dictionaries
flattened_data = []

# Loop through each game dictionary in the list
for game_dict in game_odds_data:
    # Extract the ScoreID and PregameOdds list for each game
    score_id = game_dict.get("ScoreId", None)
    pregame_odds_list = game_dict.get("PregameOdds", [])

    # Loop through each pregame odds dictionary in the PregameOdds list
    for pregame_odds_dict in pregame_odds_list:
        # Create a new flattened dictionary by combining the game dictionary and the specific pregame odds dictionary
        # Exclude the original nested PregameOdds list from the game dictionary
        flattened_dict = {k: v for k, v in game_dict.items() if k != "PregameOdds"}
        flattened_dict.update(pregame_odds_dict)
        flattened_dict["ScoreId"] = score_id  # Ensure ScoreID is kept as a common identifier

        # Add the flattened dictionary to the list
        flattened_data.append(flattened_dict)

# Display the first few flattened dictionaries to verify
# print(flattened_data[:2])
# Convert the flattened JSON data to a DataFrame
flattened_df = pd.DataFrame(flattened_data)

# Check the first few rows to see if there are any more nested structures
print(flattened_df.head())



# List of columns that uniquely identify each game and type of bet
grouping_columns = ['ScoreId', 'Season', 'SeasonType', 'Week', 'Day', 'DateTime', 'Status',
                    'AwayTeamId', 'HomeTeamId', 'AwayTeamName', 'HomeTeamName',
                    'GlobalGameId', 'GlobalAwayTeamId', 'GlobalHomeTeamId',
                    'HomeTeamScore', 'AwayTeamScore', 'TotalScore', 'HomeRotationNumber',
                    'AwayRotationNumber', 'OddType']

# Correct the column names for betting data to be averaged, removing spaces to match actual DataFrame column names
betting_columns_corrected = ['HomeMoneyLine', 'AwayMoneyLine', 'HomePointSpread', 'AwayPointSpread',
                             'HomePointSpreadPayout', 'AwayPointSpreadPayout', 'OverUnder', 'OverPayout', 'UnderPayout']

# Group the DataFrame by the unique identifiers and calculate the mean for the betting data
averaged_df = flattened_df.groupby(grouping_columns)[betting_columns_corrected].mean().reset_index()

# Display the first few rows of the averaged DataFrame
print(averaged_df.head())

# Round the betting columns to the nearest whole number and convert them to integers
averaged_df[betting_columns_corrected] = averaged_df[betting_columns_corrected].round(0).astype(int)

# Display the first few rows of the DataFrame to confirm the changes
print(averaged_df.head())

csv_output_file_path = 'X:/Personal_Project/bdn_portfolio/rl_dfs/app/data/CSV_DIR/2022_week-17__Game_Odds_Flattened.csv'
averaged_df.to_csv(csv_output_file_path, index=False)