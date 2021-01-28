import json
import re
from bs4 import BeautifulSoup
import requests
from item_hash import *

with open('items_ammos.json') as infile:
    itemList = json.load(infile)

URL = "https://terraria.gamepedia.com/Ammunition_items"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
table = soup.findAll("table", class_="terraria")
rows = table[4].findAll("tr")
for row in rows[1::]:
    cols = row.findAll("td")
    if (cols[0].text == "42") or (cols[0].text == "71"):
        continue
    else:
        ammoDict = {
            "id": "",
            "Used in": "",
            "Damage": "",
            "Velocity": "",
            "Multiplier": "",
            "Knockback": "",
            "Rarity": "",
            "recipes": []
        }
        ammoDict["id"] = cols[0].text
        
    

'''with open('items_ammos.json', "w+") as outfile:
    json.dump(itemList, outfile, indent=4)'''

