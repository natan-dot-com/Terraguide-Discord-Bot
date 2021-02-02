#Everything seems to work.
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
from scraping_tools import *
from json_manager import *
import re
import requests
from bs4 import BeautifulSoup

ITEM_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_tools.json"
FISHING_POLES = [
    "Wood Fishing Pole", "Reinforced Fishing Pole", "Fisher of Souls", "Fleshcatcher",
    "Scarab Fishing Rod", "Chum Caster", "Fiberglass Fishing Pole", "Mechanic's Rod",
    "Sitting Duck's Fishing Pole", "Hotline Fishing Hook", "Golden Fishing Rod"
]

itemList = LoadJSONFile(ITEM_FILE_PATH)
url = "https://terraria.gamepedia.com/"
jsonList = []

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Tool":
        newURL = url + itemInstance[SCRAPING_NAME].replace(" ", "_")
        print("Processing " + newURL + " with ID " + itemInstance[SCRAPING_ID])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")

        if not itemInstance[SCRAPING_NAME] in FISHING_POLES:
            tableBox = soup.find("div", class_="infobox item")
            toolDict = get_statistics(tableBox, itemInstance)
            jsonList.append(toolDict)
            
        #get fishing poles
        else:
            trTags = soup.find("table", id="fishing-poles-table").find_all("tr")
            for trTag in trTags[1:]:
                tdTags = trTag.find_all("td")
                if tdTags[1].span.span.span.text == itemInstance[SCRAPING_NAME]:
                    toolDict = {
                        SCRAPING_ITEM_ID: "",
                        SCRAPING_NAME: "",
                        SCRAPING_RARITY: "",
                        SCRAPING_VELOCITY: "",
                        SCRAPING_FISHING_POWER: "",
                        SCRAPING_SOURCES: SOURCE_SOURCES_DICT
                    }
                    
                    toolDict[SCRAPING_ITEM_ID] = itemInstance[SCRAPING_ID]
                    toolDict[SCRAPING_NAME] = itemInstance[SCRAPING_NAME]
                    toolDict[SCRAPING_FISHING_POWER] = tdTags[3].text.rstrip()
                    toolDict[SCRAPING_VELOCITY] = tdTags[4].text.rstrip()
                    toolDict[SCRAPING_RARITY] = (re.search("-*\d+", tdTags[6].a["title"])).group()
                    statistics = soup.find("div", class_="infobox item").find("div", class_="section statistics").find_all("tr")
                    for statistic in statistics:
                        if statistic.th.text == SCRAPING_USE_TIME:
                            toolDict[SCRAPING_USE_TIME] = statistic.td.text.rstrip()
                    jsonList.append(toolDict)
                    break

SaveJSONFile(ITEM_PATH_OUTPUT, jsonList)