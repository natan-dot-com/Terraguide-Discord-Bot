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
SEEDS_PATH = GLOBAL_JSON_PATH + "items_seeds.json"

itemList = LoadJSONFile(ITEM_FILE_PATH)
pylonsList = []

newURL = URL + "Seeds"
pageSeeds = requests.get(newURL)
soupSeeds = BeautifulSoup(pageSeeds.content, "html.parser")

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Seeds":
        newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        print("processing {}".format(newURL))
        tableBoxes = soup.find_all("div", class_="infobox item")
        tableBox = tableBoxes[0]
        for tableBoxTmp in tableBoxes:
            if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                tableBox = tableBoxTmp
        
        seedDict = get_statistics(tableBox, itemInstance=itemInstance)

        seedDict.pop(SCRAPING_SOURCES, None)
        seedsTables = soupSeeds.find_all("table", class_="terraria")
        found = 0
        for seedsTable in seedsTables:
            seedsTags = seedsTable.find_all("tr")
            for seedsRows in seedsTags[1:]:
                if seedsRows.find("td").find("img")["alt"] == itemInstance[SCRAPING_NAME]:
                    seedDict[SCRAPING_CREATES] = seedsRows.find_all("td")[1].text.rstrip()
                    seedDict[SCRAPING_PLANTED_IN] = seedsRows.find_all("td")[2].text.rstrip()
                    found = 1
                    break
            if found:
                break
        
        seedDict[SCRAPING_SOURCES] = SOURCE_SOURCES_DICT
        pylonsList.append(seedDict)
    
SaveJSONFile(SEEDS_PATH, pylonsList)
