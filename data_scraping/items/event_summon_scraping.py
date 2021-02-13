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

exceptionSuffix = "/Eternia_Crystal"
mainURLsuffix = "/Consumables#Summoning_items"
itemScrappingData = ["Tooltip", "Rarity"]
scrappingData = ["Item", "Event", "Notes"]
EVENT_SUMMON_PATH = GLOBAL_JSON_PATH + EVENT_SUMMON_NAME_FILE + JSON_EXT
dictList = []

itemList = LoadJSONFile('../../json/items.json')

baseURL = "https://terraria.gamepedia.com"
html = requests.get(baseURL + mainURLsuffix)
soup = BeautifulSoup(html.content, 'html.parser')
tables = soup.findAll("table", class_="terraria")
for table in tables:
    if table.caption:
        if table.caption.text == "Event-summoning items\n":
            rightTable = table
            break
rows = rightTable.findAll("tr")
index = getTableColumns(table.findAll("th"), scrappingData)
for row in rows[1::]:
    cols = row.findAll("td")
    eventDict = {
        SCRAPING_ITEM_ID: "",
        SCRAPING_RARITY: "",
        SCRAPING_EVENT: "",
        SCRAPING_TOOLTIP: "",
        SCRAPING_NOTES: "",
        SCRAPING_SOURCES: SOURCE_SOURCES_DICT
    }

    eventDict[SCRAPING_ITEM_ID] = searchForID(cols[index["Item"]].img['alt'], itemList)

    itemURLprefix = row.find("td", class_="il2c").a['href']
    itemHtml = requests.get(baseURL + itemURLprefix)
    itemSoup = BeautifulSoup(itemHtml.content, 'html.parser')
    itemTable = itemSoup.find("table", class_="stat")
    itemIndex = getTableColumns(itemTable.findAll("th"), itemScrappingData)
    itemRows = itemTable.findAll("td")

    eventDict[SCRAPING_RARITY] = re.search("\d+", itemRows[itemIndex["Rarity"]].img['alt']).group()

    eventTooltip = itemRows[itemIndex["Tooltip"]].text.split("\'")
    string = ""
    for tooltip in eventTooltip:
        if len(eventTooltip) > 1:
            if tooltip != "":
                string += tooltip + ". "
                eventDict[SCRAPING_TOOLTIP] = string[:-2]
        else:
            eventDict[SCRAPING_TOOLTIP] = tooltip + "."
    
    eventDict[SCRAPING_EVENT] = cols[index["Event"]+1].a['title']
    eventDict[SCRAPING_NOTES] = cols[index["Notes"]+1].text.replace("\n", "")
    dictList.append(eventDict)

# Eternia Crystal threatment
html = requests.get(baseURL + exceptionSuffix)
soup = BeautifulSoup(html.content, 'html.parser')
table = soup.find("table", class_="stat")
rows = table.findAll("td")
index = getTableColumns(table.findAll("th"), itemScrappingData)
eventDict = {
    SCRAPING_ITEM_ID: "",
    SCRAPING_RARITY: "",
    SCRAPING_EVENT: "",
    SCRAPING_TOOLTIP: "",
    SCRAPING_NOTES: "",
    SCRAPING_SOURCES: SOURCE_SOURCES_DICT
}
eventDict[SCRAPING_ITEM_ID] = searchForID("Eternia Crystal", itemList)
eventDict[SCRAPING_RARITY] = re.search("\d+", rows[index["Rarity"]].img['alt']).group()
eventDict[SCRAPING_EVENT] = "Old's One Army"
eventDict[SCRAPING_TOOLTIP] = re.sub(r'(Crystal)', r'\1.', rows[index["Tooltip"]].text) + "."
removeEmptyFields(eventDict)
dictList.append(eventDict)

SaveJSONFile(EVENT_SUMMON_PATH, sorted(dictList, key = lambda i: int(i[SCRAPING_ITEM_ID])))
