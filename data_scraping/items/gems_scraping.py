#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import re
import requests

IN_STONE_SUFFIX = "_In_Stone.png"
PLACED_SUFFIX = "_Placed.png"
JSON_PATH = "gems.json"

SuffixList = [IN_STONE_SUFFIX, PLACED_SUFFIX]
colsList = [2, 4]
dictInfoList = ['In Stone', 'Placed']

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
            "ID": "",
            "Rarity": "1",
            "In Stone": "",
            "Placed": ""
        }
        getID = re.search("\d+", (cols[0].find("div", class_="id").text))
        gemDict['ID'] = getID.group()
        
        gemName = cols[0].find("img")['alt']
        for suffixIdentity, colsIdentity, dictInfoIdentity in zip(SuffixList, colsList, dictInfoList):
            imgSrc = cols[colsIdentity].find("img")['src']
            imgPath = "gems/" + gemName + suffixIdentity
            
            imgOutput = requests.get(imgSrc, stream=True)
            if imgOutput.ok:
                with open(imgPath, "wb+") as handler:
                    for block in imgOutput.iter_content(1024):
                        if not block:
                            break
                        handler.write(block)
            gemDict[dictInfoIdentity] = imgPath
        gemDictList.append(gemDict)
SaveJSONFile(JSON_PATH, sorted(gemDictList, key = lambda i: i['ID']))


