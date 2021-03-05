# Load 3-level parent directories
from importlib import import_module
import path_manager
if __name__ == '__main__' and __package__ == None:
    __package__ = path_manager.importParents(level=3)
    import_module(__package__)

# Setting the root directory as working directory for Linux systems
from platform import system
from pathlib import Path
import os
systemOS = system()
if systemOS == "Linux":
    os.chdir("../../../")

from ...package.scraping_tools import *
from ...package.json_manager import *
from bs4 import BeautifulSoup
import re
import requests

BAIT_PATH = GLOBAL_JSON_PATH + BAIT_NAME_FILE + JSON_EXT
mainURLsuffix = "/Bait"
scrappingData = ["Item", "Power", "Rarity"]
dictList = []

itemList = LoadJSONFile(GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)

baseURL = "https://terraria.gamepedia.com"
html = requests.get(baseURL + mainURLsuffix)
soup = BeautifulSoup(html.content, 'html.parser')
table = soup.find("table", class_="terraria")
rows = table.findAll("tr")
index = getTableColumns(table.findAll("th"), scrappingData)
for row in rows[1::]:
    cols = row.findAll("td")
    baitDict = {
        SCRAPING_ITEM_ID: "",
        SCRAPING_RARITY: "",
        SCRAPING_BAIT_POWER: "",
        SCRAPING_SOURCE: {
            SOURCE_RECIPES: [],
            SOURCE_NPC: [],
            SOURCE_DROP: [],
            SOURCE_GRAB_BAG: [],
            SOURCE_OTHER: ""
        }
    }

    baitDict[SCRAPING_ITEM_ID] = searchForID(cols[index["Item"]].img['alt'], itemList)

    baitDict[SCRAPING_RARITY] = re.search("\d+", cols[index["Rarity"]+1].img['alt']).group()
    baitDict[SCRAPING_BAIT_POWER] = cols[index["Power"]+1].text.replace("\n", "")

    if row.find("td", class_="il2c").find("a")['title'] != "Item IDs":
        newSuffix = row.find("td", class_="il2c").a['href']
        newHtml = requests.get(baseURL + newSuffix)
        newSoup = BeautifulSoup(newHtml.content, 'html.parser')
        newTable = newSoup.find("div", class_="infobox npc c-normal critter")
        if not newTable:
            newTable = newSoup.find("div", class_="infobox npc c-normal gold critter")
        if newTable:
            newTable = newTable.find("table", class_="stat")
            newIndexes = getTableColumns(newTable.findAll("th"), ["Environment"])
            newRows = newTable.findAll("td")
            if (newIndexes["Environment"] != -1):
                baitDict[SCRAPING_SOURCE][SOURCE_OTHER] = "Found in " + newRows[newIndexes["Environment"]].a['title']
    print(baitDict)
    dictList.append(baitDict)

SaveJSONFile(BAIT_PATH, sorted(dictList, key = lambda i: int(i[SCRAPING_ITEM_ID])))
