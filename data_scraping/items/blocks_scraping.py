#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
from bs4 import BeautifulSoup
import requests

ITEMS_BLOCK_PATH = GLOBAL_JSON_PATH + "items_blocks.json"
URL = "https://terraria.gamepedia.com/"

itemList = LoadJSONFile(ITEM_FILE_PATH)
blockList = []

blockCounter = 0
for itemInstance in itemList:
    if itemInstance["Type"] == "Block":
        newURL = URL + itemInstance["Name"].replace(" ", "_")
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        table = soup.find("table", class_="stat")
        if table:
            jsonDict = {
                "Item ID": "",
                "Name": "",
                "Placeable": "",
                "Rarity": "",
                "Research": "",
                "Recipes": []
            }
            jsonDict["Item ID"] = itemInstance["ID"]
            jsonDict["Name"] = itemInstance["Name"]
            
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
