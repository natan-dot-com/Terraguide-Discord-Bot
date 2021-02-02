#Everything seems to work.

import os,sys,inspect
import re
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
import requests
from bs4 import BeautifulSoup

ARMOR_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_armors.json"
REJECTED_ARMORS = {"Empty Bucket", "Boots of Ostara", "Ultrabright Helmet"}
REJECTED_SETS = {"Dragon armor", "Titan armor", "Spectral armor"}

wikiURL = "https://terraria.gamepedia.com/"
armorList = []

newURL = wikiURL + "Armor"
page = requests.get(newURL)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all("table", class_="terraria")

itemSets = LoadJSONFile(GLOBAL_JSON_PATH + "sets.json")

#first and second tables
for table in tables[0:2]:
    trTags = table.find_all("tr")

    for trTag in trTags[2:]:
        if trTag.find_all("td")[1].a.text in REJECTED_SETS:
            continue
        newURL = wikiURL + trTag.find_all("td")[1].a.text.replace(" ", "_")
        print("processing {}".format(newURL))
        page2 = requests.get(newURL)
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        tableBoxes = soup2.find_all("div", class_="infobox item")
        processedItems = []

        for tableBox in tableBoxes:
            if re.search("armor|set", tableBox.find("div", class_="title").text, re.IGNORECASE):
                continue
            if tableBox.find("div", class_="title").text in processedItems:
                continue

            status = {
                SCRAPING_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_SET_ID: ""
            }
            status[SCRAPING_ID] = tableBox.find("div", class_="section ids").find("li").b.text
            status[SCRAPING_NAME] = tableBox.find("div", class_="title").text

            for set in itemSets:
                if tableBox.find("div", class_="title").text in set[SCRAPING_SET_PIECES]:
                    status[SCRAPING_SET_ID] = str(set[SCRAPING_ID])
                    break

            armorDict = get_statistics(tableBox, itemInstance=status, isArmor=True)
            processedItems.append(armorDict[SCRAPING_NAME])
            armorList.append(armorDict)

#third and fourth tables
for table in tables[2:-1]:
    trTags = table.find_all("tr")
    processedItems = []

    for trTag in trTags[1:]:
        newURL = wikiURL + trTag.find_all("td")[1].a.text.replace(" ", "_")
        print("processing {}".format(newURL))
        page2 = requests.get(newURL)
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        tableBox = soup2.find("div", class_="infobox item")

        if tableBox.find("div", class_="title").text in processedItems:
            continue
        
        armorDict = get_statistics(tableBox, isArmor=True)
        processedItems.append(armorDict[SCRAPING_NAME])
        armorList.append(armorDict)

#last table
trTags = tables[-1].find_all("tr")
processedItems = []
for trTag in trTags[1:]:
    if trTag.find_all("td")[1].a.text in REJECTED_ARMORS:
        continue
    
    newURL = wikiURL + trTag.find_all("td")[1].a.text.replace(" ", "_")
    print("processing {}".format(newURL))
    page2 = requests.get(newURL)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    tableBox = soup2.find("div", class_="infobox item")

    if tableBox.find("div", class_="title").text in processedItems:
        continue
    
    armorDict = get_statistics(tableBox, isArmor=True)
    processedItems.append(armorDict[SCRAPING_NAME])
    armorList.append(armorDict)

for armor in armorList:
    for set in itemSets:
        if armor[SCRAPING_NAME] in set[SCRAPING_SET_PIECES]:
            armor[SCRAPING_SET_ID] = str(set[SCRAPING_ID])
            break

SaveJSONFile(ARMOR_PATH_OUTPUT, armorList)
