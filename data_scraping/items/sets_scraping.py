#Minor output formatation issues. Aside that everything seems to work

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

SETS_PATH_OUTPUT = GLOBAL_JSON_PATH + "sets.json"
REJECTED_SETS = {"Dragon armor", "Titan armor", "Spectral armor"}
OTHER_VERSIONS = {"Console Version", "Old-gen console version", "Mobile version"}

wikiURL = "https://terraria.gamepedia.com/"
setsList = []

newURL = wikiURL + "Armor"
page = requests.get(newURL)
soup = BeautifulSoup(page.content, 'html.parser')
tables = soup.find_all("table", class_="terraria")
setID = 1

for table in tables[0:2]:
    trTags = table.find_all("tr")

    for trTag in trTags[2:]:
        if trTag.find_all("td")[1].a.text in REJECTED_SETS:
            continue
        newURL = wikiURL + trTag.find_all("td")[1].a.text.replace(" ", "_")
        print("Processing {}".format(newURL))
        page2 = requests.get(newURL)
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        tableBoxes = soup2.find_all("div", class_="infobox item")

        setDict = {}
        processedItems = []
        for tableBox in tableBoxes:
            tableTitle = tableBox.find("div", class_="title")
            if re.search("set|armor", tableTitle.text, re.IGNORECASE) and tableTitle.find("img", alt=OTHER_VERSIONS):
                print("Ignoring " + tableBox.find("div", class_="title").text)
                continue
            
            if re.search("armor", tableTitle.text, re.IGNORECASE):
                setDict[SCRAPING_ID] = str(setID)
                setID += 1
                setDict[SCRAPING_SET_NAME] = tableTitle.text.rstrip()
                statistics = tableBox.find("div", class_="section statistics").find_all("tr")
                for statistic in statistics:
                    if statistic.th.text == SCRAPING_SET_BONUS:
                        if statistic.td.find("span", class_="i"):
                            setTexts = statistic.td.find_all("i")
                            setImgs = statistic.td.find_all("span")
                            dictText = ""
                            for setText, setImg in zip(setTexts, setImgs):
                                if setImg["class"] == ["eico"]:
                                    dictText += setText.text.encode("ascii", "ignore").decode().rstrip() + " / "
                                else:
                                    dictText += setImg.img["alt"] + ": " + BeautifulSoup(str(setText).replace("<br/>", " "), 'html.parser').text.encode("ascii", "ignore").decode().rstrip() + " / "
                            setDict[SCRAPING_SET_BONUS] = dictText[:-3]
                        else:
                            if statistic.td.find("span"):
                                setTexts = statistic.td.find_all("i")
                                dictText = ""
                                for setText in setTexts:
                                    dictText += setText.text.encode("ascii", "ignore").decode().rstrip() + ", "
                                setDict[SCRAPING_SET_BONUS] = dictText[:-2]
                            else:
                                setDict[SCRAPING_SET_BONUS] = BeautifulSoup(str(statistic.td).replace("<br/>", ", "), 'html.parser').text.split("/")[0].encode("ascii", "ignore").decode().replace(",,", ",").replace(" ,", ",").rstrip()
                    elif statistic.th.text == SCRAPING_DEFENSE:
                        if statistic.td.find("span", class_="i"):
                            setTexts = statistic.td.text.split("(set)")[0].split("/")
                            setImgs = statistic.td.find_all("span", class_="i")
                            dictText = ""
                            for setText, setImg in zip(setTexts, setImgs):
                                dictText += setImg.img["alt"] + setText.encode("ascii", "ignore").decode().rstrip().replace(":", ": ").replace(" :", ":") + " / "
                            setDict[SCRAPING_DEFENSE] = dictText[:-3]
                        else:
                            setDict[SCRAPING_DEFENSE] = statistic.td.text.split(" ")[0].encode("ascii", "ignore").decode().rstrip().replace(":", "")
                    elif statistic.th.text == SCRAPING_RARITY:
                        setDict[SCRAPING_RARITY] = (re.search("-*\d+", statistic.td.span.a["title"])).group()
            else:
                if not SCRAPING_SET_PIECES in setDict.keys():
                    setDict[SCRAPING_SET_PIECES] = []
                if not tableTitle.text in processedItems:
                    setDict[SCRAPING_SET_PIECES].append(tableTitle.text)
                    processedItems.append(tableTitle.text)
            
        setsList.append(setDict)


SaveJSONFile(SETS_PATH_OUTPUT, setsList)
