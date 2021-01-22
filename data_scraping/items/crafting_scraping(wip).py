import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
from bs4 import BeautifulSoup
import requests
import json
import re

URL = "https://terraria.gamepedia.com/Iron_Pickaxe"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
counter = 1

craftingTable = soup.find("div", class_="crafts")
if craftingTable:
    rows = craftingTable.findAll("tr")
    for row in rows[1::]:
        mainDict = {
            "id": "",
            "table": [],
            "recipe": [] 
        }
        mainDict["id"] = str(counter)
        
        # Finding which item it's being crafted
        if row.find("td", class_="result"):
            result = row.find("td", class_="result").img['alt']
        
        # Finding all ingredients with its respective quantities relative to the recipe
        if row.find("td", class_="ingredients"):
            ingredientsList = row.find("td", class_="ingredients").findAll("li")
            for ingredient in ingredientsList:
                ingredientsDict = {
                    "ingredient": "",
                    "qty": ""
                }
                ingredientsDict["ingredient"] = ingredient.img['alt']
                qty = ingredient.find("span", class_="note-text")
                if qty:
                    ingredientsDict["qty"] = ' '.join(re.findall("\((\d+)\)", qty.text))
                else:
                    ingredientsDict["qty"] = '1'
                mainDict["recipe"].append(ingredientsDict)
                
        # Finding all the crating stations in which recipe can be made
        if row.find("td", class_="station"):
            stationList = row.find("td", class_="station").findAll("span", class_="i")
        for station in stationList:
            mainDict["table"].append(station.span.span.a.text)
            
        print(json.dumps(mainDict, indent=4))
        counter += 1
