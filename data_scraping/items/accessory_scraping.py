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
ACCESSORY_PATH = GLOBAL_JSON_PATH + ACCESSORY_NAME_FILE + JSON_EXT

itemList = LoadJSONFile(ITEM_FILE_PATH)
accessoriesList = []

@start_threads_decorator(size=len(itemList), threads_number=8)
def accessoriesScraping(init, fin, threadID):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Accessory":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("Thread {}: Processing {} with ID {}".format(threadID, newURL, itemInstance[SCRAPING_ID]))
        
            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            accessoriesList.append(get_statistics(tableBox, itemInstance=itemInstance))
              
    
SaveJSONFile(ACCESSORY_PATH, sortListOfDictsByKey(accessoriesList, SCRAPING_ITEM_ID))