import csv
import json

# https://api.sportsdata.io/v3/nfl/projections/json/PlayerGameProjectionStatsByWeek/2019REG/1?key=517b12cf76dc49d0a14d0a15b2b64ead
with open('1_2019(1).json', 'r') as jsonfile:
    data = json.load(jsonfile)
fieldnames = data[0].keys()
print(fieldnames)

with open('S_2019_G_1_1.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
        writer.writerow(row)

print("CSV conversion completed and saved to 'S_2020_G_1.csv'")