#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import requests

ITEMS_BLOCK_PATH = GLOBAL_JSON_PATH + "items_bricks.json"
URL = "https://terraria.gamepedia.com/"
URL_BRICKS = "Bricks"
BRICKS_IMAGE_PATH = "data_scraping/bricks_img/{}.png"

itemList = LoadJSONFile(ITEM_FILE_PATH)
bricksList = []

pageBricks = requests.get(URL + URL_BRICKS)
soupBricks = BeautifulSoup(pageBricks.content, "html.parser")
bricksRows = soupBricks.find("table").find_all("tr")[1:]

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Brick":
        newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        print("processing {}".format(newURL))

        tableBoxes = soup.find_all("div", class_="infobox item")
        tableBox = tableBoxes[0]
        for tableBoxTmp in tableBoxes:
            if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                tableBox = tableBoxTmp
        brickDict = get_statistics(tableBox, itemInstance=itemInstance)

        brickDict.pop(SCRAPING_SOURCES, None)
        for bricksRow in bricksRows:
            if bricksRow.find_all("td")[0].a["title"] == itemInstance[SCRAPING_NAME]:
                brickDict[SCRAPING_DESTROYED_BY_EXPLOSIVES] = bricksRow.find_all("td")[3].img["alt"]
                break

        brickDict[SCRAPING_SOURCES] = SOURCE_SOURCES_DICT
        bricksList.append(brickDict)

SaveJSONFile(ITEMS_BLOCK_PATH, bricksList)