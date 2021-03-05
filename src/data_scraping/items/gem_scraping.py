#Everything seems to work.

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

IN_STONE_SUFFIX = "_In_Stone.png"
PLACED_SUFFIX = "_Placed.png"
GEM_IMAGE_DIRECTORY = "gems/"
GEM_PATH = GLOBAL_JSON_PATH + GEM_NAME_FILE + JSON_EXT

SuffixList = [IN_STONE_SUFFIX, PLACED_SUFFIX]
colsList = [2, 4]
dictInfoList = [IMAGE_IN_STONE, IMAGE_PLACED]

URL = "https://terraria.gamepedia.com/Gems"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
table = soup.find("table", class_="terraria")
if table:
    gemDictList = []
    rows = table.findAll("tr")
    for row in rows[1::]:
        cols = row.findAll("td")
        gemDict = {
            SCRAPING_ITEM_ID: "",
            SCRAPING_RARITY: "1",
            IMAGE_IN_STONE: "",
            IMAGE_PLACED: ""
        }
        getID = re.search("\d+", (cols[0].find("div", class_="id").text))
        gemDict[SCRAPING_ITEM_ID] = getID.group()
        print("Getting information from ID " + gemDict[SCRAPING_ITEM_ID])
        
        gemName = cols[0].find("img")['alt']
        for suffixIdentity, colsIdentity, dictInfoIdentity in zip(SuffixList, colsList, dictInfoList):
            imgSrc = cols[colsIdentity].find("img")['src']
            imgPath =  GEM_IMAGE_DIRECTORY + gemName + suffixIdentity
            
            imgOutput = requests.get(imgSrc, stream=True)
            if imgOutput.ok:
                with open(GLOBAL_JSON_PATH + imgPath, "wb+") as handler:
                    for block in imgOutput.iter_content(1024):
                        if not block:
                            break
                        handler.write(block)
            gemDict[dictInfoIdentity] = imgPath
        gemDictList.append(gemDict)
SaveJSONFile(GEM_PATH, sorted(gemDictList, key = lambda i: i[SCRAPING_ITEM_ID]))


