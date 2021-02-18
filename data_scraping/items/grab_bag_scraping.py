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

mainURLsuffix = "/Grab_bags"
cratesURLsuffix = "/Crates"
treasureBagURLsuffix = "/Treasure_bag"

SORTABLE_TABLE_CLASS = "sortable"
GRAB_BAG_PATH = GLOBAL_JSON_PATH + GRAB_BAG_FILE + JSON_EXT
cratesScrappingData = [
    "Pre-Hardmode type", "Hardmode type", "Sell", 
    "Rarity", "Biome", "Catch quality"
]
scrappingData = ["Source"]

def getTableContent(urlSuffix, tableClass):
    baseURL = "https://terraria.gamepedia.com"
    html = requests.get(baseURL + urlSuffix)
    soup = BeautifulSoup(html.content, 'html.parser')
    table = soup.find("table", class_=tableClass)
    return table

def cratesScrap(cratesTable, dictList):
    tableRows = cratesTable.findAll("tr")
    tableHead = getTableColumns(tableRows[0].findAll("th"), cratesScrappingData)
    cratesList = ["Pre-Hardmode type", "Hardmode type"]
    for row in tableRows[1::]:
        tableCols = row.findAll("td")
        for idColumn in cratesList:
            bagDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_RARITY: "",
                SCRAPING_SELL: "",
                SCRAPING_CATCH_QUALITY: "",
                SCRAPING_BAG_DROPS: [],
                SCRAPING_SOURCE: {
                    SOURCE_RECIPES: [],
                    SOURCE_NPC: [],
                    SOURCE_DROP: [],
                    SOURCE_GRAB_BAG: [],
                    SOURCE_OTHER: ""
                }
            }
            
            divText = tableCols[tableHead[idColumn]].find("div", class_="id").text
            bagDict[SCRAPING_ITEM_ID] = re.search("\d+", divText).group()

            rarityTitle = tableCols[tableHead["Rarity"]].a['title']
            bagDict[SCRAPING_RARITY] = re.search("\d+", rarityTitle).group()

            bagDict[SCRAPING_SELL] = tableCols[tableHead["Sell"]].span['title']
            bagDict[SCRAPING_CATCH_QUALITY] = tableCols[tableHead["Catch quality"]].text.strip().replace(" [2]", "")

            # Crate source
            middleString = tableCols[tableHead["Biome"]].a
            if middleString:
                sourceString = "Fishing in " + middleString['title']
            else:
                sourceString = "Fishing in any biome"
            bagDict[SCRAPING_SOURCE][SOURCE_OTHER] = sourceString

            dictList.append(bagDict)

def main():
    dictList = []
    cratesTable = getTableContent(cratesURLsuffix, SORTABLE_TABLE_CLASS)
    cratesScrap(cratesTable, dictList)
    print(json.dumps(dictList, indent=4))
    #SaveJSONFile(GRAB_BAG_PATH, sorted(dictList, key = lambda i: int(i[SCRAPING_ITEM_ID])))

if __name__ == "__main__":
    main()