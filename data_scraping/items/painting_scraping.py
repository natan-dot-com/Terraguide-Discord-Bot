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

IMAGE_EXTENSION = ".png"
DIRECTORY = "paintings/"
JSON_PATH = "items_paintings.json"
dictList = []

itemList = LoadJSONFile('../../json/items.json')

URL = "https://terraria.gamepedia.com/Pets#Light_Pets"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
tables = soup.findAll("table", class_="terraria")
for table in tables:
    rows = table.findAll("tr")
    for row in rows[1::]:
        paintingDict = {
            SCRAPING_ITEM_ID: "",
            SCRAPING_PLACED: "",
            SCRAPING_TOOLTIP: "",
            SCRAPING_DESCRIPTION: "",
            SCRAPING_SOURCE: SOURCE_SOURCES_DICT
        }

SaveJSONFile(JSON_PATH, sorted(dictList, key = lambda i: int(i[SCRAPING_ITEM_ID])))
