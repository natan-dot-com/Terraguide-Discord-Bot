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

ITEMS_BLOCK_PATH = GLOBAL_JSON_PATH + "items_consumables.json"
URL = "https://terraria.gamepedia.com/"

LIQUID_BOMBS = {"Dry Bomb", "Wet Bomb", "Lava Bomb", "Honey Bomb"}

itemList = LoadJSONFile(ITEM_FILE_PATH)
consumablesList = []

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Consumable":
        newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        print("processing {}".format(newURL))

        if not itemInstance[SCRAPING_NAME] in LIQUID_BOMBS:
            tableBox = soup.find("div", class_="infobox item")
            consumableDict = get_statistics(tableBox, itemInstance=itemInstance)
            #Remove Sell key from Vine rope
            if itemInstance[SCRAPING_NAME] == "Vine Rope":
                consumableDict.pop("Sell", None)
            consumablesList.append(consumableDict)
        #If item is a liquid bomb
        else:
            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            consumablesList.append(get_statistics(tableBox, itemInstance=itemInstance))

SaveJSONFile(ITEMS_BLOCK_PATH, consumablesList)