import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import requests

URL = "https://terraria.gamepedia.com/"
PYLON_PATH = GLOBAL_JSON_PATH + "items_pylons.json"

itemList = LoadJSONFile(ITEM_FILE_PATH)
pylonsList = []

newURL = URL + "Pylons"
page = requests.get(newURL)
soup = BeautifulSoup(page.content, "html.parser")

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Pylon":
        tableBox = soup.find("div", class_="infobox item")
        pylonDict = get_statistics(tableBox, itemInstance=itemInstance)

        pylonTable = soup.find("table", class_="terraria").find_all("tr")
        for pylonRow in pylonTable[1:]:
            if pylonRow.find("td", class_="il1c").img["alt"] == itemInstance[SCRAPING_NAME]:
                pylonDict.pop(SCRAPING_SOURCES, None)
                if pylonRow.find("sup"):
                    pylonDict[SCRAPING_USABLE] = pylonRow.find_all("td")[6].contents[0].rstrip()
                else:
                    pylonDict[SCRAPING_USABLE] = pylonRow.find_all("td")[6].text.rstrip()
        
        pylonDict[SCRAPING_SOURCES] = SOURCE_SOURCES_DICT
        pylonsList.append(pylonDict)
    
SaveJSONFile(PYLON_PATH, pylonsList)
