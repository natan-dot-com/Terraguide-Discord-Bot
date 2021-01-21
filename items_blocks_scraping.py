from bs4 import BeautifulSoup
import requests
import json
from json_manager import *

ITEMS_BLOCK_PATH = 'json_new/items_blocks.json'
URL = "https://terraria.gamepedia.com/"

itemList = LoadJSONFile('json_new/items.json')
blockList = []

blockCounter = 0
for itemInstance in itemList:
    if itemInstance['type'] == "Block":
        newURL = URL + itemInstance['name'].replace(" ", "_")
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        table = soup.find("table", class_="stat")
        if table:
            jsonDict = {
                "id": "",
                "name": "",
                "Placeable": "",
                "Rarity": "",
                "Research": "",
                "recipes": []
            }
            jsonDict['id'] = itemInstance['id']
            jsonDict['name'] = itemInstance['name']
            
            placement = table.find("a", title="Placement")
            if placement:
                jsonDict['Placeable'] = placement.parent.parent.img['alt']
                
            rarity = table.find("span", class_="rarity")
            if rarity:
                jsonDict['Rarity'] = rarity.a['title'][-1]
                
            research = table.find("abbr", title="Journey Mode")
            if research:
                jsonDict['Research'] = research.text
            else:
                jsonDict['Research'] = "n/a"
                
            print(jsonDict)
            blockList.append(jsonDict)
            blockCounter += 1
        
SaveJSONFile(ITEMS_BLOCK_PATH, blockList)
