from app.switches import dispatch_converter

data_types = ['Player_Projection_Stats', 'Player_Actual_Stats', 'Team_Stats', 'Game_Odds']

count = 0
total_data_type = len(data_types)
weeks_per_season = 18
season_interest_start = 2012
season_interest_end = 2023
total_seasons = season_interest_end - season_interest_start

# 11 x 4 x 18
total_request = total_data_type * total_seasons * weeks_per_season
def data_conversion(target_type, target_season, target_week):
    target_type = target_type
    target_season = target_season
    target_week = target_week

    print(f' {target_season} | {target_week} | {target_type} ')
    tag_name = f'{target_season}_week-{target_week}__{target_type}'
    json_file_path = f'data_json/{tag_name}.json'
    csv_file_path = f'data_csv/{tag_name}.csv'

    conversion_controller = "Sports_Book" if target_type == "Game_Odds" else "Sports_Data"
    print(conversion_controller)

    # dispatch_cleaner("" ,target_type, target_season, target_week)
    dispatch_converter(conversion_controller, json_file_path, csv_file_path)


# def state_handler(notifier):
#     message = notifier
#     completion = False if message is not "done" else True
#     if completion:
#         return message
#     print(message)
#     return completion
