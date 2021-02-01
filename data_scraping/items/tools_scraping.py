#Everything seems to work.
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
from scraping_tools import *
from json_manager import *
import re
import requests
from bs4 import BeautifulSoup

ITEM_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_tools.json"
FISHING_POLES = [
    "Wood Fishing Pole", "Reinforced Fishing Pole", "Fisher of Souls", "Fleshcatcher",
    "Scarab Fishing Rod", "Chum Caster", "Fiberglass Fishing Pole", "Mechanic's Rod",
    "Sitting Duck's Fishing Pole", "Hotline Fishing Hook", "Golden Fishing Rod"
]

itemList = LoadJSONFile(ITEM_FILE_PATH)
url = "https://terraria.gamepedia.com/"
jsonList = []

for item in itemList:
    if item[SCRAPING_TYPE] == "Tool":
        newURL = url + item[SCRAPING_NAME].replace(" ", "_")
        print("Processing " + newURL + " with ID " + item[SCRAPING_ID])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")

        if not item[SCRAPING_NAME] in FISHING_POLES:
            table = soup.find("div", class_="infobox item")
            if table:
                jsonDict = {
                    SCRAPING_ITEM_ID: "",
                    SCRAPING_NAME: "",
                    SCRAPING_RARITY: "",
                    SCRAPING_USE_TIME: "",
                    SCRAPING_VELOCITY: "",
                    SCRAPING_TOOL_SPEED: "",
                    SCRAPING_PICKAXE_POWER: "",
                    SCRAPING_HAMMER_POWER: "",
                    SCRAPING_AXE_POWER: "",
                    SCRAPING_FISHING_POWER: "",
                    SCRAPING_SOURCES: SOURCE_SOURCES_DICT
                }
                jsonDict[SCRAPING_ITEM_ID] = item[SCRAPING_ID]
                jsonDict[SCRAPING_NAME] = item[SCRAPING_NAME]

                rarity = table.find("span", class_="rarity")
                if rarity:
                    jsonDict[SCRAPING_RARITY] = (re.search("-*\d+", rarity.a["title"])).group()

                use_time = table.find("span", class_="usetime")
                if use_time:
                    use_time = use_time.parent
                    jsonDict[SCRAPING_USE_TIME] = use_time.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()

                tool_speed = table.find("a", title="Mining speed")
                if tool_speed:
                    tool_speed = tool_speed.parent.parent.find("td")
                    jsonDict[SCRAPING_TOOL_SPEED] = tool_speed.text.split(" ", 1)[0]

                power = table.find("ul", class_="toolpower")
                if power:
                    powerList = power.find_all("li")
                    for powerType in powerList:
                        if(powerType["title"] == "Pickaxe power"):
                            jsonDict[SCRAPING_PICKAXE_POWER] = powerType.text[1:].split(" ", 1)[0]
                        elif(powerType["title"] == "Hammer power"):
                            jsonDict[SCRAPING_HAMMER_POWER] = powerType.text[1:].split(" ", 1)[0]
                        elif(powerType["title"] == "Axe power"):
                            jsonDict[SCRAPING_AXE_POWER] = powerType.text[1:].split(" ", 1)[0]

                jsonList.append(jsonDict)
        else:
            trTags = soup.find("table", id="fishing-poles-table").find_all("tr")
            for trTag in trTags[1:]:
                tdTags = trTag.find_all("td")
                if tdTags[1].span.span.span.text == item["Name"]:
                    jsonDict = {
                        SCRAPING_ITEM_ID: "",
                        SCRAPING_NAME: "",
                        SCRAPING_RARITY: "",
                        SCRAPING_USE_TIME: "",
                        SCRAPING_VELOCITY: "",
                        SCRAPING_TOOL_SPEED: "",
                        SCRAPING_PICKAXE_POWER: "",
                        SCRAPING_HAMMER_POWER: "",
                        SCRAPING_AXE_POWER: "",
                        SCRAPING_FISHING_POWER: "",
                        SCRAPING_SOURCES: SOURCE_SOURCES_DICT
                    }
                    
                    jsonDict[SCRAPING_ITEM_ID] = item[SCRAPING_ID]
                    jsonDict[SCRAPING_NAME] = item[SCRAPING_NAME]
                    jsonDict[SCRAPING_FISHING_POWER] = tdTags[3].text.rstrip()
                    jsonDict[SCRAPING_VELOCITY] = tdTags[4].text.rstrip()
                    jsonDict[SCRAPING_RARITY] = (re.search("-*\d+", tdTags[6].a["title"])).group()
                    statistics = soup.find("div", class_="infobox item").find("div", class_="section statistics").find_all("tr")
                    for statistic in statistics:
                        if statistic.th.text == SCRAPING_USE_TIME:
                            jsonDict[SCRAPING_USE_TIME] = statistic.td.text.rstrip()
                    jsonList.append(jsonDict)
                    break

SaveJSONFile(ITEM_PATH_OUTPUT, jsonList)