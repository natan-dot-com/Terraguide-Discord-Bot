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

JSON_PATH = "items_shields.json"
itemList = LoadJSONFile("../../json/items.json")
shieldsList = []

URL = "https://terraria.gamepedia.com/Shields"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
table = soup.find("table", class_="terraria")
if table:
    rows = table.findAll("tr")
    for row in rows[2::]:
        cols = row.findAll("td")
        if cols:
            shieldsDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_EFFECT: [],
                SCRAPING_SOURCE: SOURCE_SOURCES_DICT
            }
            shieldsDict[SCRAPING_ITEM_ID] = searchForID(cols[0].find("img")['alt'], itemList)
            shieldEffects = cols[2].findAll("li")
            for effect in shieldEffects:
                if effect.text:
                    shieldsDict[SCRAPING_EFFECT].append(effect.text.replace("\n", "").replace("\"", "").strip())
            shieldsList.append(shieldsDict)
            # It's needed to take Cobalt Shield's source manually
SaveJSONFile(JSON_PATH, sorted(shieldsList, key = lambda i: int(i[SCRAPING_ITEM_ID])))


