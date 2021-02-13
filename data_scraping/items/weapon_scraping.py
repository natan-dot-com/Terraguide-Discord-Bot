
#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
import requests
from bs4 import BeautifulSoup

WEAPON_PATH = GLOBAL_JSON_PATH + WEAPON_NAME_FILE + JSON_EXT
ITEM_URL = ["Enchanted Sword"]

itemList = LoadJSONFile(GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)
url = "https://terraria.gamepedia.com/"
weaponsList = []

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Weapon":
        newURL = url + itemInstance[SCRAPING_NAME].replace(" ", "_")
        if itemInstance[SCRAPING_NAME] in ITEM_URL:
            newURL += "_(item)"
        print("Processing " + newURL + " with ID " + itemInstance[SCRAPING_ID])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        tableBox = soup.find("div", class_="infobox item")

        weaponsList.append(get_statistics(tableBox, itemInstance))

SaveJSONFile(WEAPON_PATH, weaponsList)
