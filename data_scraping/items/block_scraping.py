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

BLOCK_PATH = GLOBAL_JSON_PATH + BLOCK_NAME_FILE + JSON_EXT
URL = "https://terraria.gamepedia.com/"

itemList = LoadJSONFile(ITEM_FILE_PATH)
blockList = []

blockCounter = 0
for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Block":
        newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        print("processing {}".format(newURL))

        tableBox = soup.find("div", class_="infobox item")
        blockList.append(get_statistics(tableBox, itemInstance=itemInstance))
        blockCounter += 1
        
SaveJSONFile(BLOCK_PATH, blockList)
