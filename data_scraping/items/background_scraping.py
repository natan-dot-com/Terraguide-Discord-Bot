import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
from scraping_tools import *
from json_manager import *
import requests
from bs4 import BeautifulSoup

BACKGROUND_PATH = GLOBAL_JSON_PATH + BACKGROUND_NAME_FILE + JSON_EXT
WALLS_SUBTYPES = {
    "Stained Glass", "Wallpapers", "Fences", "Gemstone Walls",
    "Cave Walls", "Mossy Walls", "Sandstone Walls", "Corruption Walls"
}
DUNGEON_WALLS = {
    "Blue Brick Wall", "Green Brick Wall", "Pink Brick Wall",
    "Blue Slab Wall", "Green Slab Wall", "Pink Slab Wall",
    "Blue Tiled Wall", "Green Tiled Wall", "Pink Tiled Wall"
}
itemList = LoadJSONFile(GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)
url = "https://terraria.gamepedia.com/"
wallsList = []

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Background":
        newURL = url + itemInstance[SCRAPING_NAME].replace(" ", "_")
        print("Processing " + newURL + " with ID " + itemInstance[SCRAPING_ID])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")

        if not itemInstance[SCRAPING_NAME] in DUNGEON_WALLS:
            tableBoxes = soup.find_all("div", class_="infobox item")
        elif itemInstance[SCRAPING_NAME] in DUNGEON_WALLS:       
            tableBoxes = soup.find_all("div", class_="infobox item float-left")
        else:
            tableBoxes = soup.find_all("div", class_="infobox npc c-normal background object")

        #find the correct wall table
        tableBox = tableBoxes[0]
        for tableBoxTmp in tableBoxes:
            if tableBoxTmp.find("div", class_="title").text in WALLS_SUBTYPES:
                tableBox = tableBoxTmp
                break

        wallDict = get_statistics(tableBox, itemInstance)
        wallsList.append(wallDict)

SaveJSONFile(BACKGROUND_PATH, wallsList)
