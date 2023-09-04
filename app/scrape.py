import csv
import json
import os
from dotenv import load_dotenv

load_dotenv(".env")
url = os.getenv("URL_SECRET")
api_key = os.getenv("KEY_SECRET")

data_type= "2019REG/1?key="

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