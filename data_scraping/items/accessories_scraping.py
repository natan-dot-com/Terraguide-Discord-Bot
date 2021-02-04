import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import requests
from multithreading_starter import *

URL = "https://terraria.gamepedia.com/"
ACCESSORY_PATH = GLOBAL_JSON_PATH + "items_accessories.json"

itemList = LoadJSONFile(ITEM_FILE_PATH)
accessoriesList = []

def accessoriesScraping(init, fin, threadID):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Accessory":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("processing {} on thread {}".format(newURL, threadID))
        
            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            accessoriesList.append(get_statistics(tableBox, itemInstance=itemInstance))
              
    
start_threads(__file__, accessoriesScraping.__name__, len(itemList), 8)
SaveJSONFile(ACCESSORY_PATH, sortListOfDictsByKey(accessoriesList, SCRAPING_ITEM_ID))
exit(0)