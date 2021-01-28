#Need to fix duplicates

import os,sys,inspect
import re
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
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

        for tableBox in tableBoxes:
            if re.search("armor|set", tableBox.find("div", class_="title").text, re.IGNORECASE):
                continue

            armorDict = {
                "Item ID": "",
                "Set ID": "",
                "Name": "",
                "Defense": "",
                "Body Slot": "",
                "Tooltip": "",
                "Rarity": "",
                "Research": "",
                "Recipes": [] 
            }

            armorDict["Item ID"] = tableBox.find("div", class_="section ids").find("li").b.text
            armorDict["Name"] = tableBox.find("div", class_="title").text
            statistics = tableBox.find("div", class_="section statistics").find_all("tr")
            for statistic in statistics:
                if statistic.th.text == "Defense":
                    armorDict["Defense"] = statistic.td.text.split(" ")[0]
                elif statistic.th.text == "Body slot":
                    armorDict["Body Slot"] = statistic.td.text
                elif statistic.th.text == "Tooltip":
                    armorDict["Tooltip"] = statistic.td.text.split("/")[0].rstrip()
                elif statistic.th.text == "Rarity":
                    armorDict["Rarity"] = statistic.td.span.a["title"][-1]
                elif statistic.th.text == "Research":
                    armorDict["Research"] = statistic.td.text
            
            armorList.append(armorDict)

#third and fourth tables
for table in tables[2:-1]:
    trTags = table.find_all("tr")

    for trTag in trTags[1:]:
        newURL = wikiURL + trTag.find_all("td")[1].a.text.replace(" ", "_")
        print("processing {}".format(newURL))
        page2 = requests.get(newURL)
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        tableBox = soup2.find("div", class_="infobox item")

        armorDict = {
            "Item ID": "",
            "Set ID": "",
            "Name": "",
            "Defense": "",
            "Body Slot": "",
            "Tooltip": "",
            "Rarity": "",
            "Research": "",
            "Recipes": [] 
        }
        armorDict["Item ID"] = tableBox.find("div", class_="section ids").find("li").b.text
        armorDict["Name"] = tableBox.find("div", class_="title").text
        statistics = tableBox.find("div", class_="section statistics").find_all("tr")
        for statistic in statistics:
            if statistic.th.text == "Defense":
                armorDict["Defense"] = statistic.td.text.split(" ")[0]
            elif statistic.th.text == "Body slot":
                armorDict["Body Slot"] = statistic.td.text
            elif statistic.th.text == "Tooltip":
                armorDict["Tooltip"] = statistic.td.text.split("/")[0].rstrip()
            elif statistic.th.text == "Rarity":
                armorDict["Rarity"] = statistic.td.span.a["title"][-1]
            elif statistic.th.text == "Research":
                armorDict["Research"] = statistic.td.text
        
        armorList.append(armorDict)

#last table
trTags = tables[-1].find_all("tr")

for trTag in trTags[1:]:
    if trTag.find_all("td")[1].a.text in REJECTED_ARMORS:
        continue
    newURL = wikiURL + trTag.find_all("td")[1].a.text.replace(" ", "_")
    print("processing {}".format(newURL))
    page2 = requests.get(newURL)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    tableBox = soup2.find("div", class_="infobox item")

    armorDict = {
        "Item ID": "",
        "Set ID": "",
        "Name": "",
        "Defense": "",
        "Body Slot": "",
        "Tooltip": "",
        "Rarity": "",
        "Research": "",
        "Recipes": [] 
    }
    armorDict["Item ID"] = tableBox.find("div", class_="section ids").find("li").b.text
    armorDict["Name"] = tableBox.find("div", class_="title").text
    statistics = tableBox.find("div", class_="section statistics").find_all("tr")
    for statistic in statistics:
        if statistic.th.text == "Defense":
            armorDict["Defense"] = statistic.td.text.split(" ")[0]
        elif statistic.th.text == "Body slot":
            armorDict["Body Slot"] = statistic.td.text
        elif statistic.th.text == "Tooltip":
            armorDict["Tooltip"] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.split("/")[0].rstrip()
        elif statistic.th.text == "Rarity":
            armorDict["Rarity"] = statistic.td.span.a["title"][-1]
        elif statistic.th.text == "Research":
            armorDict["Research"] = statistic.td.text
    
    armorList.append(armorDict)

SaveJSONFile(ARMOR_PATH_OUTPUT, armorList)
