# Still wip: Need to get the items that each npc sells

#Load 3-level parent directories
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
    os.chdir("../../")

from ...package.scraping_tools import *
from ...package.json_manager import *
from ...package.item_hash import *
from bs4 import BeautifulSoup
import requests

TOWN_NPC_PATH = GLOBAL_JSON_PATH + NPC_TOWN_NAME_FILE + JSON_EXT
MAIN_URL = "https://terraria.gamepedia.com"
TOWN_NPC_SUFFIX = "/NPCs"
tableHeadLabels = ["NPC", "Description", "Spawn requirement"]

def initializeHashTables():
    npcList = LoadJSONFile(GLOBAL_JSON_PATH + NPC_NAME_FILE + JSON_EXT)
    npcHash = hashTable(NPC_HASH_SIZE, SCRAPING_NAME)
    for npcInstance in npcList:
        npcHash.add(npcInstance[SCRAPING_NAME], npcInstance)

    return npcHash

def scrapGeneralInformation(townList, npcHash):
    html = requests.get(MAIN_URL + TOWN_NPC_SUFFIX)
    soup = BeautifulSoup(html.content, 'html.parser')
    tableList = soup.findAll("table", class_=TERRARIA_TABLE_CLASS)
    for table in tableList[:4:]:
        if tableList.index(table) == 2:
            continue

        rowList = table.findAll("tr")
        tableHead = getTableColumns(rowList[0].findAll("th"), tableHeadLabels)
        for row in rowList[1::]:
            colList = row.findAll("td")
            townDict = {
                NPC_ID: "",
                SCRAPING_DESCRIPTION: "",
                SCRAPING_SPAWN_REQUIREMENT: "",
                NPC_SELL_LIST: []
            }
            npcName = colList[tableHead["NPC"]].img['alt']
            print("Getting information from '" + npcName + "'.")
            townDict[NPC_ID] = npcHash.search(npcName, NPC_ID)
            townDict[SCRAPING_DESCRIPTION] = colList[tableHead["Description"]+1].text.strip()

            spawnReqString = colList[tableHead["Spawn requirement"]+1].text.replace("\u2009", "").replace("\u00a0",
                                                                                                          "").replace("\u2013",
                                                                                                                     "-")
            townDict[SCRAPING_SPAWN_REQUIREMENT] = spawnReqString.strip()
            townList.append(townDict)

def main():
    townList = []
    IDcounter = 1

    npcHash = initializeHashTables()
    scrapGeneralInformation(townList, npcHash)
    SaveJSONFile(TOWN_NPC_PATH, townList)

if __name__ == "__main__":
    main()
