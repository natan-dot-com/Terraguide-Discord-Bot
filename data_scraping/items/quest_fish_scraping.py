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

QUEST_FISH_PATH = GLOBAL_JSON_PATH + QUEST_FISH_NAME_FILE + JSON_EXT
questFishDictList = []

URL = "https://terraria.gamepedia.com/Angler/Quests"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
table = soup.find("table", class_="terraria")
rows = table.findAll("tr")
for row in rows[1::]:
    cols = row.findAll("td")
    questFishDict = {
        SCRAPING_ITEM_ID: "",
        SCRAPING_RARITY: "-11",
        SCRAPING_HEIGHT: "",
        SCRAPING_BIOME: "",
        SCRAPING_ANGLER_QUOTE: ""
    }
    string = cols[0].text
    questFishDict[SCRAPING_ANGLER_QUOTE] = string[:string.find("(")]
    questFishDict[SCRAPING_ITEM_ID] = re.search("\d+", cols[2].find("div", class_="id").text).group()
    questFishDict[SCRAPING_HEIGHT] = cols[3].text.replace("\n", "")
    questFishDict[SCRAPING_BIOME] = cols[4].text.replace("\n", "").replace("[1]", "")
    questFishDictList.append(questFishDict)
SaveJSONFile(QUEST_FISH_PATH, sorted(questFishDictList, key = lambda i: int(i[SCRAPING_ITEM_ID])))

