import requests
import csv
import json
import os
from dotenv import load_dotenv as ld_env
from modules.dot_export import secrets

env_path = os.path.abspath("../.env")

secret_var = secrets(env_path)
entry, player_projected_pts, player_actual_pts, team_performance, odds, access = secret_var

print(secret_var)


# print(f'{entry}{data_one}{}')



#
season = 2019
week = 1
#
url = f'{entry}/{odds}/{season}REG/{week}?key={access}'
print(url)
# data_type = "2019REG/1?key="
#
# with open('player_stat_by_week.json', 'r') as jsonfile:
#     data = json.load(jsonfile)
# fieldnames = data[0].keys()
# print(fieldnames)
# print(data)
#
# with open('S_2019_G_1_1.csv', 'w', newline='') as csvfile:
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for row in data:
#         writer.writerow(row)
#
# print("CSV conversion completed and saved to 'S_2020_G_1.csv'")