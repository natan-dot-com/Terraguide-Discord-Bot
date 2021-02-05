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
STORAGE_PATH = GLOBAL_JSON_PATH + BOSS_SUMMON_JSON_NAME_FILE
newURL = URL + "Consumables"
pageConsumables = requests.get(newURL)
soupConsumables = BeautifulSoup(pageConsumables.content, "html.parser")

itemList = LoadJSONFile(ITEM_FILE_PATH)
bossSummonsList = []

@start_threads_decorator(size=len(itemList), threads_number=8)
def bossSummonsScraping(init, fin, threadID):
    for itemInstance in itemList[init:fin]:
        if itemInstance[SCRAPING_TYPE] == "Boss summon":
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("Thread {}: Processing {} with ID {}".format(threadID, newURL, itemInstance[SCRAPING_ID]))
        
            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            bossSummonDict = get_statistics(tableBox, itemInstance=itemInstance)

            bossSummonDict.pop(SCRAPING_SOURCES)
            bossSummonRows = soupConsumables.find_all("table")[4].find_all("tr")[1:]
            for bossSummonRow in bossSummonRows:
                if bossSummonRow.find("td").find("img")["alt"] == itemInstance[SCRAPING_NAME]:
                    bossSummonDict[SCRAPING_SUMMONS] = bossSummonRow.find_all("td")[2].text.strip()
                    bossSummonDict[SCRAPING_USABLE] = bossSummonRow.find_all("td")[3].text.strip()

            bossSummonDict[SCRAPING_SOURCES] = SOURCE_SOURCES_DICT
            bossSummonsList.append(bossSummonDict)
              
SaveJSONFile(STORAGE_PATH, sortListOfDictsByKey(bossSummonsList, SCRAPING_ITEM_ID))