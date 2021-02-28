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
from bs4 import BeautifulSoup
import requests

# Execution commands
GET_NPC_PAGE_LINK = True
GET_NPC_IMAGES = False

# Constant values
MAIN_NPC_FILE_PATH = GLOBAL_JSON_PATH + NPC_NAME_FILE + JSON_EXT
MAIN_URL = "https://terraria.gamepedia.com"
URL_CATEGORY_SUFFIXES = {
    "Enemies": '/Enemies',
    "Critters": '/Critters',
    "NPCs": '/NPCs',
    "Bosses": '/Bosses'
}

def scrapEnemiesPage(npcList, IDcounter):
    if GET_NPC_PAGE_LINK:
        linkDict = {}

    html = requests.get(MAIN_URL + URL_CATEGORY_SUFFIXES["Enemies"])
    soup = BeautifulSoup(html.content, 'html.parser')
    divList = soup.findAll("div", class_="itemlist")
    if divList:
        for divInstance in divList[:-2:]:
            liList = divInstance.findAll("li")
            for liInstance in liList:
                npcTableDict = {
                    NPC_ID: "",
                    SCRAPING_NAME: "",
                    SCRAPING_TYPE: ""
                }
                npcImage = liInstance.a.img
                
                npcTableDict[NPC_ID] = str(IDcounter)
                npcTableDict[SCRAPING_NAME] = npcImage['alt']
                npcTableDict[SCRAPING_TYPE] = "Enemy"
                
                if GET_NPC_PAGE_LINK:
                    linkDict[npcTableDict[NPC_ID]] = npcImage.parent['href']
                
                if GET_NPC_IMAGES:
                    filePath = GLOBAL_JSON_PATH + IMAGE_DIR_NPC + npcTableDict[SCRAPING_NAME].lower().replace(" ", "_") + \
                    STATIC_IMAGE_EXT
                    writeImage(npcImage['src'], filePath)
                    
                npcList.append(npcTableDict)
                IDcounter += 1
                
        if GET_NPC_PAGE_LINK:
            SaveJSONFile("enemy_linkdict.json", linkDict)

def scrapCrittersPage(npcList, IDcounter):
    pass

def scrapTownNPCPage(npcList, IDcounter):
    pass

def scrapBossesPage(npcList, IDcounter):
    pass

def main():
    if GET_NPC_IMAGES:
        if not os.path.exists(GLOBAL_JSON_PATH + IMAGE_DIR_NPC):
            Path(GLOBAL_JSON_PATH + IMAGE_DIR_NPC).mkdir(parents=True, exist_ok=True)

    npcList = []
    functionList = [
        scrapEnemiesPage,
        scrapCrittersPage,
        scrapTownNPCPage,
        scrapBossesPage
    ]

    IDcounter = 1
    for functionInstance in functionList:
        functionInstance(npcList, IDcounter)
        IDcounter = len(npcList)+1
    SaveJSONFile(MAIN_NPC_FILE_PATH, npcList)

if __name__ == '__main__':
    main()
