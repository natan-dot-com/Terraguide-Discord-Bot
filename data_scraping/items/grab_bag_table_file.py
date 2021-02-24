import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import re
import requests

bagList = LoadJSONFile("../../" + GLOBAL_JSON_PATH + GRAB_BAG_NAME_FILE + JSON_EXT)
itemList = LoadJSONFile("../../" + GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)

newList = []
IDcounter = 1
for bagInstance in bagList:
    newDict = {
        BAG_ID: "",
        SCRAPING_NAME: "",
        GRAB_BAGS_LOOT_LIST: [],
    } 
    newDict[BAG_ID] = str(IDcounter)
    newDict[SCRAPING_NAME] = itemList[int(bagInstance[SCRAPING_ITEM_ID])-1][SCRAPING_NAME]
    print("Processing " + newDict[SCRAPING_NAME]) 
    newList.append(newDict)
    IDcounter += 1
SaveJSONFile("../../" + GLOBAL_JSON_PATH + BAGS_NAME_FILE + JSON_EXT, newList)
