#

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import requests
import threading
import math
from multithreading_starter import *

FURNITURE_PATH = GLOBAL_JSON_PATH + FURNITURE_NAME_FILE + JSON_EXT
URL = "https://terraria.gamepedia.com/"
BRICKS_IMAGE_PATH = "data_scraping/bricks_img/{}.png"
OTHER_FOUNDS = ["Dungeon", "Obsidian"]
OTHER_FOUNDS_SOURCE = ["Found in the Dungeon", "Found in Ruined Houses, in the Underworld"]

itemList = LoadJSONFile(ITEM_FILE_PATH)
furnituresList = []

@start_threads_decorator(size=len(itemList), threads_number=8)
def furniturescraping(init, fin, threadID):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Furniture":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("Thread {}: Processing {} with ID {}".format(threadID, newURL, itemInstance[SCRAPING_ID]))

            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            furnitureDict = get_statistics(tableBox, itemInstance=itemInstance)

            furnitureDict.pop(SCRAPING_SOURCES)
            furnitureSourceOther = ""
            for otherFoundInstance, otherFoundSourceInstance in zip(OTHER_FOUNDS, OTHER_FOUNDS_SOURCE):
                if re.search(otherFoundInstance, itemInstance[SCRAPING_NAME]) and not re.search("Sink|Obsidian Watcher Banner", itemInstance[SCRAPING_NAME]):
                    furnitureSourceOther = otherFoundSourceInstance
                    break
                elif itemInstance[SCRAPING_NAME] == "Book":
                    furnitureSourceOther = "Found in the Dungeon"

            furnitureDict[SCRAPING_SOURCES] = {
                SOURCE_RECIPES: [],
                SOURCE_NPC: [],
                SOURCE_DROP: [],
                SOURCE_GRAB_BAG: [],
                SOURCE_OTHER: furnitureSourceOther,
            }

            furnituresList.append(furnitureDict)

SaveJSONFile(FURNITURE_PATH, sortListOfDictsByKey(furnituresList, SCRAPING_ITEM_ID))