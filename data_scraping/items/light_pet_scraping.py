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

DYNAMIC_IMAGE_ITEMS = ["Crimson Heart", "Wisp", "Suspicious Looking Eye", "Flickerwick", "Jack 'O Lantern", "Toy Golem", "Fairy Princess"]
IMAGE_EXTENSION = ".png"
DYNAMIC_IMAGE_EXTENSION = ".gif"
DIRECTORY = "light_pets/"
JSON_PATH = "items_light_pet.json"
dictList = []

itemList = LoadJSONFile('../../json/items.json')

URL = "https://terraria.gamepedia.com/Pets#Light_Pets"
html = requests.get(URL)
soup = BeautifulSoup(html.content, 'html.parser')
tables = []
tables.append(soup.find("table", { "id" : "table-Light-Pets"}))
tables.append(soup.find("table", { "id" : "table-Master-Mode-Light-Pets"}))
if tables:
    for table in tables:
        rows = table.findAll("tr")
        for row in rows[1::]:
            cols = row.findAll("td")
            petDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_LIGHT_PET: "",
                SCRAPING_BRIGHTNESS: "",
                SCRAPING_NOTES: "",
                SCRAPING_MASTER_MODE: "",
                SCRAPING_BUFF_IMAGE: "",
                SCRAPING_PET_IMAGE: [],
                SCRAPING_SOURCE: SOURCE_SOURCES_DICT
            } 
            petDict[SCRAPING_ITEM_ID] = searchForID(cols[2].text.replace("\n", ""), itemList)
            petDict[SCRAPING_LIGHT_PET] = cols[1].text.replace("\n", "")
            petDict[SCRAPING_BRIGHTNESS] = cols[3].text.replace("\n", "")
            if len(cols) == 6:
                petDict[SCRAPING_NOTES] = cols[5].text.replace("\n", "")
            
            imagePath = DIRECTORY + cols[2].text.replace("\n", "").replace(" ", "_") + "_Buff" + IMAGE_EXTENSION
            writeImage(cols[0].find("img")['src'], imagePath)
            petDict[SCRAPING_BUFF_IMAGE] = imagePath
            
            if cols[1].text.replace("\n", "") == "Fairy":
                imageCounter = 1
                for petImage in cols[1].findAll("img"):
                    imagePath = DIRECTORY + cols[1].text.replace("\n", "").replace(" ", "_")
                    imagePath += "_" + str(imageCounter)
                    if petDict[SCRAPING_LIGHT_PET] in DYNAMIC_IMAGE_ITEMS:
                        imagePath += DYNAMIC_IMAGE_EXTENSION
                    else:
                        imagePath += IMAGE_EXTENSION
                    writeImage(petImage['src'], imagePath)
                    petDict[SCRAPING_PET_IMAGE].append(imagePath)
                    imageCounter += 1
            else:
                imagePath = DIRECTORY + cols[1].text.replace("\n", "").replace(" ", "_")
                if petDict[SCRAPING_LIGHT_PET] not in DYNAMIC_IMAGE_ITEMS:
                    imagePath += IMAGE_EXTENSION
                else:
                    imagePath += DYNAMIC_IMAGE_EXTENSION
                writeImage(cols[1].find("img")['src'], imagePath)
                petDict[SCRAPING_PET_IMAGE].append(imagePath)
            
            if tables.index(table) == 0:
                petDict[SCRAPING_MASTER_MODE] = "No"
            else:
                petDict[SCRAPING_MASTER_MODE] = "Yes"
                
            petDict = removeEmptyFields(petDict)
            dictList.append(petDict)

SaveJSONFile(JSON_PATH, sorted(dictList, key = lambda i: int(i[SCRAPING_ITEM_ID])))
