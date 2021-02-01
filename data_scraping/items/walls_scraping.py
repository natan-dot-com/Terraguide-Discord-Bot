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



def get_statistics(tableBox, itemInstance):
    wallDict = {
        SCRAPING_ITEM_ID: "",
        SCRAPING_NAME: "",
        SCRAPING_PLACEABLE: "",
        SCRAPING_USE_TIME: "",
        SCRAPING_RARITY: "",
        SCRAPING_MAX_LIFE: "",
        SCRAPING_SOURCES: SOURCE_SOURCES_DICT
    }

    wallDict[SCRAPING_ITEM_ID] = itemInstance[SCRAPING_ID]
    wallDict[SCRAPING_NAME] = itemInstance[SCRAPING_NAME]

    statistics = tableBox.find("div", class_="section statistics").find_all("tr")
    for statistic in statistics:
        if statistic.th.text == SCRAPING_USE_TIME:
            wallDict[SCRAPING_USE_TIME] = statistic.td.text.rstrip()
        elif statistic.th.text == SCRAPING_RARITY:
            wallDict[SCRAPING_RARITY] = (re.search("-*\d+", statistic.td.span.a["title"])).group()
        elif statistic.th.text == SCRAPING_PLACEABLE:
            wallDict[SCRAPING_PLACEABLE] = statistic.td.img["alt"]
        elif statistic.th.text == SCRAPING_MAX_LIFE:
            wallDict[SCRAPING_MAX_LIFE] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
    return wallDict

ITEM_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_backgrounds.json"
WALLS_SUBTYPES = {
    "Stained Glass", "Wallpapers", "Fences", "Gemstone Walls",
    "Cave Walls", "Mossy Walls", "Sandstone Walls", "Corruption Walls"
}
DUNGEON_WALLS = {
    "Blue Brick Wall", "Green Brick Wall", "Pink Brick Wall",
    "Blue Slab Wall", "Green Slab Wall", "Pink Slab Wall",
    "Blue Tiled Wall", "Green Tiled Wall", "Pink Tiled Wall"
}
EXCEPTIONS = {"Crimson Heart", "Shadow Orb"}
itemList = LoadJSONFile(ITEM_FILE_PATH)
url = "https://terraria.gamepedia.com/"
wallsList = []

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Background":
        newURL = url + itemInstance[SCRAPING_NAME].replace(" ", "_")
        print("Processing " + newURL + " with ID " + itemInstance[SCRAPING_ID])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")

        if not itemInstance[SCRAPING_NAME] in EXCEPTIONS:
            tableBoxes = soup.find_all("div", class_="infobox item")
        else:
            tableBoxes = soup.find_all("div", class_="infobox npc c-normal background object")

        #find the correct wall table
        tableBox = tableBoxes[0]
        for tableBoxTmp in tableBoxes:
            if tableBoxTmp.find("div", class_="title").text in WALLS_SUBTYPES:
                tableBox = tableBoxTmp
                break

        wallDict = get_statistics(tableBox, itemInstance)
        #fuck wiki
        if itemInstance[SCRAPING_NAME] in DUNGEON_WALLS:
            wallDict[SCRAPING_PLACEABLE] = "Yes"
        wallsList.append(wallDict)

SaveJSONFile(ITEM_PATH_OUTPUT, wallsList)
