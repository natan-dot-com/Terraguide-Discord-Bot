import json
import re
from bs4 import BeautifulSoup
import requests
from item_hash import *

with open('items.json') as infile:
    itemList = json.load(infile)

URL = "https://terraria.gamepedia.com/Lanterns"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
tables = soup.findAll("table", class_="sortable")
extra = soup.find("table", class_="terraria")
tables.append(extra)
for table in tables:
    ids = table.findAll("div", class_="id")
    for ID in ids:
        itemID = int((re.search("\d+", ID.text)).group())
        itemList[itemID-1]['type'] = "Light source"

with open('items.json', "w+") as outfile:
    json.dump(itemList, outfile, indent=4)

