#There are small string format issues on output that needed to be solved by hand

import os,sys,inspect
import re
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
import json
from tools import *
import requests
from bs4 import BeautifulSoup

JSON_PATH = "json/"
ITEMS_PATH = JSON_PATH + "items.json"
AMMO_PATH_OUTPUT = JSON_PATH + "items_ammos.json"
AMMOS_TYPES = ["Arrows", "Bullets", "Rockets", "Darts", "Solutions"]

wikiURL = "https://terraria.gamepedia.com/"
ammoList = []

for pageName in AMMOS_TYPES:
    newURL = wikiURL + pageName
    page = requests.get(newURL)
    soup = BeautifulSoup(page.content, 'html.parser')

    #for Arrows, Bullets and Darts pages
    if pageName == "Arrows" or pageName == "Bullets" or pageName == "Darts":

        items = soup.find("table", class_="terraria").find_all("tr")

        for item in items[1:]:
            ammoDict = {
                "id": "",
                "name": "",
                "Used in": "",
                "Damage": "",
                "Velocity": "",
                "Multiplier": "",
                "Knockback": "",
                "Rarity": "",
                "recipes": [] 
            }
            tdTags = item.find_all("td")

            id = item.find("div", class_="id")      
            ammoDict["id"] = (re.search("\d+", id.text)).group()
            ammoDict["name"] = item.img['alt']
            if pageName == "Arrows":
                ammoDict["Used in"] = "Any Bow or Repeater."
            elif pageName == "Bullets":
                ammoDict["Used in"] = "Any Gun"
            elif pageName == "Darts":
                ammoDict["Used in"] = "Blowgun, Blowpipe, Dart Pistol and Dart Rifle"
            ammoDict["Damage"] = tdTags[2].text.split(' ')[0].rstrip()
            if tdTags[3].text.split(' ')[0] != "???\n":
                ammoDict["Velocity"] = tdTags[3].text.split(' ')[0].rstrip()
            ammoDict["Multiplier"] = tdTags[4].text.split(' ')[0].rstrip()
            if tdTags[5].text != "???\n":
                ammoDict["Knockback"] = " (".join(tdTags[5].text.rstrip().split("("))
            ammoDict["Rarity"] = tdTags[7].a['title'].split(' ')[-1]
            #print(json.dumps(ammoDict, indent=2))
            ammoList.append(ammoDict)

    #for Rockets page
    elif pageName == "Rockets":

        items = soup.find("table", class_="terraria").find_all("tr")

        for item in items[1:]:
            ammoDict = {
                "id": "",
                "name": "",
                "Used in": "",
                "Damage": "",
                "Availability": "",
                "Rarity": "",
                "Source": "",
                "Radius": "",
                "Destroy Tiles": "",
                "Recipes": []
            }
            tdTags = item.find_all("td")

            id = item.find("div", class_="id")      
            ammoDict["id"] = (re.search("\d+", id.text)).group()
            ammoDict["name"] = item.img['alt']
            ammoDict['Used in'] = "Launcher"
            ammoDict["Damage"] = tdTags[1].text.split(' ')[0].rstrip()
            ammoDict["Availability"] = 'or '.join(tdTags[2].text.rstrip().split('or'))
            ammoDict["Rarity"] = tdTags[3].a['title'].split(' ')[-1]
            if not tdTags[2].find("img"):
                ammoDict["Source"] = tdTags[4].text.split('(')[0].rstrip()
            ammoDict["Radius"] = tdTags[5].text.rstrip()
            ammoDict["Destroy Tiles"] = tdTags[6].img['alt']
            #print(json.dumps(ammoDict, indent=2))
            ammoList.append(ammoDict)

    #for Solutions page
    elif pageName == "Solutions":

        items = soup.find("table", class_="terraria").find_all("tr")

        for item in items[1:]:
            ammoDict = {
                "id": "",
                "Available": "",
                "Effect": "",
                "Rarity": "",
                "Tooltip": ""
            }
            tdTags = item.find_all("td")
            id = item.find("div", class_="id")      
            ammoDict["id"] = (re.search("\d+", id.text)).group()
            ammoDict["name"] = item.img['alt']
            ammoDict["Available"] = " ".join((tdTags[1].text.rstrip()).split("  "))
            ammoDict["Effect"] = tdTags[2].text.rstrip()
            ammoDict["Rarity"] = "3"
            ammoDict["Tooltip"] = tdTags[3].text.rstrip()
            #print(json.dumps(ammoDict, indent=2))
            ammoList.append(ammoDict)


SaveJSONFile(AMMO_PATH_OUTPUT, ammoList)
