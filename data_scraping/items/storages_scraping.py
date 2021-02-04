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
STORAGE_PATH = GLOBAL_JSON_PATH + "items_storages.json"
STORAGE_WITH_SOURCES = [
    "Blue Dungeon Dresser", "Green Dungeon Dresser", "Pink Dungeon Dresser", "Obsidian Dresser"
]

itemList = LoadJSONFile(ITEM_FILE_PATH)
storagesList = []

def storagesScraping(init, fin, threadID):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Storage":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("processing {} on thred {}".format(newURL, threadID))
        
            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            storageDict = get_statistics(tableBox, itemInstance=itemInstance)

            storageDict.pop(SCRAPING_SOURCES)
            storageSourceOther = ""
            if itemInstance[SCRAPING_NAME] in STORAGE_WITH_SOURCES:
                newURL = URL + "Dressers"
                pageDresser = requests.get(newURL)
                soupDresser = BeautifulSoup(pageDresser.content, "html.parser")
                tableRows = soupDresser.find("table", class_="terraria lined").find_all("tr")[1:]

                for tableRow in tableRows:
                    if tableRow.find("img")["alt"] == itemInstance[SCRAPING_NAME]:
                        storageSourceOther = tableRow.find_all("td")[1].text.strip()

            elif re.search("Chest", itemInstance[SCRAPING_NAME]):
                newURL = URL + "Chests"
                pageChest = requests.get(newURL)
                soupChest = BeautifulSoup(pageChest.content, "html.parser")
                tableRows = soupChest.find("table", class_="terraria lined").find_all("tr")[1:]

                for tableRow in tableRows:
                    if tableRow.find("img")["alt"] == itemInstance[SCRAPING_NAME]:
                        textHTML = BeautifulSoup(str(tableRow.find_all("td")[1]).replace("<br/>", ","), 'html.parser')
                        storageSourceOther = "Found in " + textHTML.text.replace(" ,", ",").strip()

            storageDict[SCRAPING_SOURCES] = {
                SOURCE_RECIPES: [],
                SOURCE_NPC: [],
                SOURCE_DROP: [],
                SOURCE_GRAB_BAG: [],
                SOURCE_OTHER: storageSourceOther,
            }

            storagesList.append(storageDict)
              
    
start_threads(__file__, storagesScraping.__name__, len(itemList), 8)
SaveJSONFile(STORAGE_PATH, sortListOfDictsByKey(storagesList, SCRAPING_ITEM_ID))
exit(0)