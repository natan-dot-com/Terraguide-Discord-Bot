#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
from bs4 import BeautifulSoup
import requests

ITEMS_FISH_PATH = GLOBAL_JSON_PATH + "items_fishes.json"
URL = "https://terraria.gamepedia.com/"
FISH_URL = "Fishing_catches"
JUNK_LIST = ["Old Shoe", "Seaweed", "Tin Can"]

itemList = LoadJSONFile(ITEM_FILE_PATH)
fishesList = []
newURL = URL + FISH_URL
pageFish = requests.get(newURL)
soupFish = BeautifulSoup(pageFish.content, "html.parser")

fishTable = soupFish.find("table", class_="terraria")
fishRows = fishTable.find_all("tr")

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Fishing catches":
        if not itemInstance[SCRAPING_NAME] in JUNK_LIST:
            newURL = URL + itemInstance[SCRAPING_NAME].replace(" ", "_")
            page = requests.get(newURL)
            soup = BeautifulSoup(page.content, "html.parser")
            print("processing {}".format(newURL))

            tableBoxes = soup.find_all("div", class_="infobox item")
            tableBox = tableBoxes[0]
            for tableBoxTmp in tableBoxes:
                if tableBoxTmp.find("div", class_="title").text == itemInstance[SCRAPING_NAME]:
                    tableBox = tableBoxTmp
            fishDict = get_statistics(tableBox, itemInstance=itemInstance)

            for fishRow in fishRows[1:]:
                if fishRow.find("td", class_="il2c").find("a").text == itemInstance[SCRAPING_NAME]:
                    fishDict.pop(SCRAPING_SOURCES, None)
                    fishDict[SCRAPING_HEIGHT] = fishRow.find_all("td")[4].text.encode("ascii", "ignore").decode().rstrip()

                    textBiome = ""
                    if fishRow.find_all("td")[5].find("span", class_="eico"):
                        textBiome = fishRow.find_all("td")[5].contents[0].rstrip()
                        if re.search("\(", textBiome) and not re.search("\)", textBiome):
                            textBiome += ")"
                    else:
                        textBiome = fishRow.find_all("td")[5].text.encode("ascii", "ignore").decode().replace(" )", ")").rstrip()
                    if re.search("\[\d]", textBiome):
                        fishDict[SCRAPING_BIOME] = textBiome.replace(re.search("\[\d]", textBiome).group(), "")
                    else:
                        fishDict[SCRAPING_BIOME] = textBiome

                    textCatch = ""
                    if fishRow.find_all("td")[5].find("span", class_="eico"):
                        textCatch = fishRow.find_all("td")[6].contents[0].rstrip()
                        if re.search("\(", textCatch) and not re.search("\)", textCatch):
                            textCatch += ")"
                    else:
                        textCatch = fishRow.find_all("td")[6].text.encode("ascii", "ignore").decode().replace(" )", ")").rstrip()
                    if re.search("\[\d]", textCatch):
                        fishDict[SCRAPING_CATCH_QUALITY] = textCatch.replace(re.search("\[\d]", textCatch).group(), "")
                    else:
                        fishDict[SCRAPING_CATCH_QUALITY] = textCatch
                    fishDict[SCRAPING_SOURCES] = SOURCE_SOURCES_DICT
                    fishesList.append(fishDict)
                    break 
        else:
            fishDict = {
                SCRAPING_ITEM_ID: itemInstance[SCRAPING_ID],
                SCRAPING_NAME: itemInstance[SCRAPING_ID],
                SCRAPING_RARITY: "-1",
                SCRAPING_HEIGHT: "Any",
                SCRAPING_BIOME: "Any",
                SCRAPING_SOURCES: SOURCE_SOURCES_DICT
            }
            fishesList.append(fishDict)

SaveJSONFile(ITEMS_FISH_PATH, fishesList)