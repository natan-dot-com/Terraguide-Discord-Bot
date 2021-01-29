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

DIRECTORY = "ores/"
IMAGE_EXTENSION = ".png"
IN_STONE_SUFFIX = "_In_Stone"
JSON_PATH = "items_ore.json"
oreDictList = []

URL = "https://terraria.gamepedia.com/Ores"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
tables = soup.findAll("table", class_="terraria")

# Getting data from the first table (Relevant: ID and Rarity)
rows = tables[0].findAll("tr")
for row in rows[1::]:
    oreDict = {
        "Item ID": "",
        "Ore Tier": "",
        "Rarity": "",
        "Minimum Pickaxe Power": "",
        "In Stone": "",
        "Source": ""
    }
    cols = row.findAll("td")
    oreDict['Item ID'] = (re.search("\d+", cols[1].div.text)).group()
    oreDict['Rarity'] = (re.search("\d+", cols[2].a['title'])).group()
    oreDictList.append(oreDict)

# Getting data from the second/third table (Relevant: the other ones)
oreIndex = 0
for table in tables[1:3:]:
    rows = table.findAll("tr")
    for row in rows[1::]:
        cols = row.findAll("td")
        colsNumber = len(cols)
        
        # For when there's just one ore in the table row
        if colsNumber == 4:
            
            # Table row header (ore tier)
            oreDictList[oreIndex]['Ore Tier'] = (re.search("\d+", row.th.text)).group()
            
            # First column (image)
            colImages = cols[0].findAll("img")
            imgPath = DIRECTORY + colImages[1]['alt'].replace(" ", "_") + IN_STONE_SUFFIX + IMAGE_EXTENSION
            imgOutput = requests.get(colImages[0]['src'], stream=True)
            if imgOutput.ok:
                with open(imgPath, "wb+") as handler:
                    for block in imgOutput.iter_content(1024):
                        if not block:
                            break
                        handler.write(block)
            oreDictList[oreIndex]['In Stone'] = imgPath
            
            # Second column (pickaxe power)
            oreDictList[oreIndex]['Minimum Pickaxe Power'] = (cols[1].find("img"))['alt']
            
            # Fourth column (source)
            oreDictList[oreIndex]['Source'] = cols[3].text.replace("\n", "")
            oreIndex += 1
            
        # For when there's two ores in the same table row
        if colsNumber == 5:
            
            # Table row header (ore tier)
            oreDictList[oreIndex]['Ore Tier'] = (re.search("\d+", row.th.text)).group()
            oreDictList[oreIndex+1]['Ore Tier'] = (re.search("\d+", row.th.text)).group()
            
            # First column (first ore image)
            colImages = cols[0].findAll("img")
            imgPath = DIRECTORY + colImages[1]['alt'].replace(" ", "_") + IN_STONE_SUFFIX + IMAGE_EXTENSION
            imgOutput = requests.get(colImages[0]['src'], stream=True)
            if imgOutput.ok:
                with open(imgPath, "wb+") as handler:
                    for block in imgOutput.iter_content(1024):
                        if not block:
                            break
                        handler.write(block)
            oreDictList[oreIndex]['In Stone'] = imgPath
            
            # Second column (second ore image)
            colImages = cols[1].findAll("img")
            imgPath = DIRECTORY + colImages[1]['alt'].replace(" ", "_") + IN_STONE_SUFFIX + IMAGE_EXTENSION
            imgOutput = requests.get(colImages[0]['src'], stream=True)
            if imgOutput.ok:
                with open(imgPath, "wb+") as handler:
                    for block in imgOutput.iter_content(1024):
                        if not block:
                            break
                        handler.write(block)
            oreDictList[oreIndex+1]['In Stone'] = imgPath
            
            # Third column (pickaxe power) 
            oreDictList[oreIndex]['Minimum Pickaxe Power'] = (cols[2].find("img"))['alt']
            oreDictList[oreIndex+1]['Minimum Pickaxe Power'] = (cols[2].find("img"))['alt']
            
            # Fifth column (source)
            oreDictList[oreIndex]['Source'] = cols[4].text.replace("\n", "")
            oreDictList[oreIndex+1]['Source'] = cols[4].text.replace("\n", "")
            oreIndex += 2
            
SaveJSONFile(JSON_PATH, sorted(oreDictList, key = lambda i: int(i['Item ID'])))







