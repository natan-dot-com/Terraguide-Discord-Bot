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

scrappingData = ["Painting", "Name", "Placed", "Tooltip", "Description"]
IMAGE_EXTENSION = ".png"
DIRECTORY = "paintings/"
JSON_PATH = "items_paintings.json"
dictList = []

itemList = LoadJSONFile('../../json/items.json')

URL = "https://terraria.gamepedia.com/Paintings"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
tables = soup.findAll("table", class_="terraria")
for table in tables:
    rows = table.findAll("tr")
    index = getTableColumns(rows[0].findAll("th"), scrappingData)
    for row in rows[1::]:
        cols = row.findAll("td")
        paintingDict = {
            SCRAPING_ITEM_ID: "",
            SCRAPING_PLACED: "",
            SCRAPING_TOOLTIP: "",
            SCRAPING_DESCRIPTION: "",
            SCRAPING_SOURCE: SOURCE_SOURCES_DICT
        }
        if index["Name"] != NOT_FOUND:
            paintingDict[SCRAPING_ITEM_ID] = re.search("\d+", cols[index["Name"]].find("div", class_="id").text).group()
            
        if index["Painting"] != NOT_FOUND:
            imagePath = cols[index["Painting"]].img['alt'].replace(" ", "_") + IMAGE_EXTENSION
            writeImage(cols[index["Painting"]].img['src'], imagePath)
            
        if index["Placed"] != NOT_FOUND:
            imagePath = DIRECTORY + cols[index["Painting"]].img['alt'].replace(" ", "_") + "_Placed" + IMAGE_EXTENSION
            writeImage(cols[index["Placed"]].img['src'], imagePath)
            paintingDict[SCRAPING_PLACED] = imagePath
            
        if index["Tooltip"] != NOT_FOUND:
            paintingDict[SCRAPING_TOOLTIP] = cols[index["Tooltip"]].text.replace("\n", "")
            
        if index["Description"] != NOT_FOUND:
            paintingDict[SCRAPING_DESCRIPTION] = cols[index["Description"]].text.replace("\n", "").replace("\"", "")
           
        removeEmptyFields(paintingDict)
        dictList.append(paintingDict)
SaveJSONFile(JSON_PATH, sorted(dictList, key = lambda i: int(i[SCRAPING_ITEM_ID])))
