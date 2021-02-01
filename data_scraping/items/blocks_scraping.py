#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
import re
from bs4 import BeautifulSoup
import requests

ITEMS_BLOCK_PATH = GLOBAL_JSON_PATH + "items_blocks.json"
URL = "https://terraria.gamepedia.com/"

itemList = LoadJSONFile(ITEM_FILE_PATH)
blockList = []

blockCounter = 0
for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Block":
        newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        
        table = soup.find("table", class_="stat")
        if table:
            jsonDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_PLACEABLE: "",
                SCRAPING_RARITY: "",
                SCRAPING_RESEARCH: "",
                SCRAPING_SOURCES: SOURCE_SOURCES_DICT
            }
            jsonDict[SCRAPING_ITEM_ID] = itemInstance[SCRAPING_ID]
            jsonDict[SCRAPING_NAME] = itemInstance[SCRAPING_NAME]
            
            placement = table.find("a", title="Placement")
            if placement:
                jsonDict[SCRAPING_PLACEABLE] = placement.parent.parent.img["alt"]
                
            rarity = table.find("span", class_="rarity")
            if rarity:
                jsonDict[SCRAPING_RARITY] = (re.search("-*\d+", rarity.a["title"])).group()
                
            research = table.find("abbr", title="Journey Mode")
            if research:
                jsonDict[SCRAPING_RESEARCH] = research.text
            else:
                jsonDict[SCRAPING_RESEARCH] = "n/a"
                
            print(jsonDict)
            blockList.append(jsonDict)
            blockCounter += 1
        
SaveJSONFile(ITEMS_BLOCK_PATH, blockList)
