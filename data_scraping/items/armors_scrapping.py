#Need to fix duplicates

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

            armorDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_SET_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_DEFENSE: "",
                SCRAPING_BODY_SLOT: "",
                SCRAPING_TOOLTIP: "",
                SCRAPING_RARITY: "",
                SCRAPING_RESEARCH: "",
                SCRAPING_RECIPES: [] 
            }

            armorDict[SCRAPING_ITEM_ID] = tableBox.find("div", class_="section ids").find("li").b.text
            armorDict[SCRAPING_NAME] = tableBox.find("div", class_="title").text
            statistics = tableBox.find("div", class_="section statistics").find_all("tr")
            for statistic in statistics:
                if statistic.th.text == SCRAPING_DEFENSE:
                    armorDict[SCRAPING_DEFENSE] = statistic.td.text.split(" ")[0]
                elif statistic.th.text == "Body slot":
                    armorDict[SCRAPING_BODY_SLOT] = statistic.td.text
                elif statistic.th.text == SCRAPING_TOOLTIP:
                    armorDict[SCRAPING_TOOLTIP] = statistic.td.text.split("/")[0].rstrip()
                elif statistic.th.text == SCRAPING_RARITY:
                    armorDict[SCRAPING_RARITY] = statistic.td.span.a["title"][-1]
                elif statistic.th.text == SCRAPING_RESEARCH:
                    armorDict[SCRAPING_RESEARCH] = statistic.td.text
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

        armorDict = {
            SCRAPING_ITEM_ID: "",
            SCRAPING_SET_ID: "",
            SCRAPING_NAME: "",
            SCRAPING_DEFENSE: "",
            SCRAPING_BODY_SLOT: "",
            SCRAPING_TOOLTIP: "",
            SCRAPING_RARITY: "",
            SCRAPING_RESEARCH: "",
            SCRAPING_RECIPES: [] 
        }
        armorDict[SCRAPING_ITEM_ID] = tableBox.find("div", class_="section ids").find("li").b.text
        armorDict[SCRAPING_NAME] = tableBox.find("div", class_="title").text
        statistics = tableBox.find("div", class_="section statistics").find_all("tr")
        for statistic in statistics:
            if statistic.th.text == SCRAPING_DEFENSE:
                armorDict[SCRAPING_DEFENSE] = statistic.td.text.split(" ")[0]
            elif statistic.th.text == "Body slot":
                armorDict[SCRAPING_BODY_SLOT] = statistic.td.text
            elif statistic.th.text == SCRAPING_TOOLTIP:
                armorDict[SCRAPING_TOOLTIP] = statistic.td.text.split("/")[0].rstrip()
            elif statistic.th.text == SCRAPING_RARITY:
                armorDict[SCRAPING_RARITY] = statistic.td.span.a["title"][-1]
            elif statistic.th.text == SCRAPING_RESEARCH:
                armorDict[SCRAPING_RESEARCH] = statistic.td.text
        
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

    armorDict = {
        SCRAPING_ITEM_ID: "",
        SCRAPING_SET_ID: "",
        SCRAPING_NAME: "",
        SCRAPING_DEFENSE: "",
        SCRAPING_BODY_SLOT: "",
        SCRAPING_TOOLTIP: "",
        SCRAPING_RARITY: "",
        SCRAPING_RESEARCH: "",
        SCRAPING_RECIPES: [] 
    }
    armorDict[SCRAPING_ITEM_ID] = tableBox.find("div", class_="section ids").find("li").b.text
    armorDict[SCRAPING_NAME] = tableBox.find("div", class_="title").text
    statistics = tableBox.find("div", class_="section statistics").find_all("tr")
    for statistic in statistics:
        if statistic.th.text == SCRAPING_DEFENSE:
            armorDict[SCRAPING_DEFENSE] = statistic.td.text.split(" ")[0]
        elif statistic.th.text == "Body slot":
            armorDict[SCRAPING_BODY_SLOT] = statistic.td.text
        elif statistic.th.text == SCRAPING_TOOLTIP:
            armorDict[SCRAPING_TOOLTIP] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.split("/")[0].rstrip()
        elif statistic.th.text == SCRAPING_RARITY:
            armorDict[SCRAPING_RARITY] = statistic.td.span.a["title"][-1]
        elif statistic.th.text == SCRAPING_RESEARCH:
            armorDict[SCRAPING_RESEARCH] = statistic.td.text
    
    processedItems.append(armorDict[SCRAPING_NAME])
    armorList.append(armorDict)

itemSets = LoadJSONFile(GLOBAL_JSON_PATH + "sets.json")
for armor in armorList:
    for set in itemSets:
        if armor[SCRAPING_NAME] in set[SCRAPING_SET_PIECES]:
            armor[SCRAPING_SET_ID] = str(set[SCRAPING_ID])
            break

SaveJSONFile(ARMOR_PATH_OUTPUT, armorList)
