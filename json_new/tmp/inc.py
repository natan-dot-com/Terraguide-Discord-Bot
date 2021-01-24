import json
import re
from bs4 import BeautifulSoup
import requests
from item_hash import *

targetList = []

URL = "https://terraria.gamepedia.com/Lanterns"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
tables = soup.findAll("table", class_="terraria")
for table in tables:
    rows = table.findAll("tr")
    for row in rows[1::]:
        targetList.append(row.img['alt'])

with open('items.json', "r") as infile:
    itemList = json.load(infile)

itemHash = hashTable(8192, 'name')
for item in itemList:
    itemHash.add(item['name'], item)

for target in targetList:
    ID = int(itemHash.search(target, 'id'))
    if ID != NOT_FOUND:
        itemList[ID-1]['type'] = "Light source"
        print(itemList[ID-1]['name'])

with open('items.json', "w+") as outfile:
    json.dump(itemList, outfile, indent=4)
