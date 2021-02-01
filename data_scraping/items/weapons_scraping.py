
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

ITEM_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_weapons.json"
ITEM_URL = ["Enchanted Sword"]

itemList = LoadJSONFile(ITEM_FILE_PATH)
url = "https://terraria.gamepedia.com/"
jsonList = []

for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == "Weapon":
        newURL = url + itemInstance[SCRAPING_NAME].replace(" ", "_")
        if itemInstance[SCRAPING_NAME] in ITEM_URL:
            newURL += "_(item)"
        print("Processing " + newURL + " with ID " + itemInstance[SCRAPING_ID])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("div", class_="infobox item")

        if table:
            jsonDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_DAMAGE: "",
                SCRAPING_KNOCKBACK: "",
                SCRAPING_MANA: "",
                SCRAPING_CRITICAL_CHANCE: "",
                SCRAPING_USE_TIME: "",
                SCRAPING_VELOCITY: "",
                SCRAPING_RARITY: "",
                SCRAPING_RESEARCH: "",
                SCRAPING_SOURCES: SOURCE_SOURCES_DICT 
            }
            jsonDict[SCRAPING_ITEM_ID] = itemInstance[SCRAPING_ID]
            jsonDict[SCRAPING_NAME] = itemInstance[SCRAPING_NAME]

            damage = table.find("th", text=SCRAPING_DAMAGE)
            if damage:
                jsonDict[SCRAPING_DAMAGE] = damage.parent.td.text.split(" ")[0]

            knockback = table.find("span", class_="knockback")
            if knockback:
                jsonDict[SCRAPING_KNOCKBACK] = knockback.parent.text.split("/")[0].rstrip()

            mana = table.find("a", title=SCRAPING_MANA)
            if mana:
                jsonDict[SCRAPING_MANA] = mana.parent.parent.td.text.split(" ")[0]

            critical_chance = table.find("a", title="Critical hit")
            if critical_chance:
                jsonDict[SCRAPING_CRITICAL_CHANCE] = critical_chance.parent.parent.td.text.split(" ")[0]

            use_time = table.find("span", class_="usetime")
            if use_time:
                use_time = use_time.parent
                jsonDict[SCRAPING_USE_TIME] = use_time.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()

            velocity = table.find("a", title=SCRAPING_VELOCITY)
            if velocity:
                jsonDict[SCRAPING_VELOCITY] = velocity.parent.parent.td.text.split(" ")[0]

            rarity = table.find("span", class_="rarity")
            if rarity:
                jsonDict[SCRAPING_RARITY] = (re.search("-*\d+", rarity.a["title"])).group()

            research = table.find("a", title="Journey mode")
            if research:
                jsonDict[SCRAPING_RESEARCH] = research.parent.parent.td.text

            jsonList.append(jsonDict)

SaveJSONFile(ITEM_PATH_OUTPUT, jsonList)
