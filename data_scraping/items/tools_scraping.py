#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
import requests
from bs4 import BeautifulSoup

ITEM_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_tools.json"
FISHING_POLES = [
    "Wood Fishing Pole", "Reinforced Fishing Pole", "Fisher of Souls", "Fleshcatcher",
    "Scarab Fishing Rod", "Chum Caster", "Fiberglass Fishing Pole", "Mechanic's Rod",
    "Sitting Duck's Fishing Pole", "Hotline Fishing Hook", "Golden Fishing Rod"
]

itemList = LoadJSONFile(ITEM_FILE_PATH)
url = "https://terraria.gamepedia.com/"
jsonList = []

for item in itemList:
    if item["Type"] == "Tool":
        newURL = url + item["Name"].replace(" ", "_")
        print("Processing " + newURL + " with ID " + item["ID"])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")

        if not item["Name"] in FISHING_POLES:
            table = soup.find("div", class_="infobox item")
            if table:
                jsonDict = {
                    "Item ID": "",
                    "Name": "",
                    "Rarity": "",
                    "Use Time": "",
                    "Velocity": "",
                    "Tool Speed": "",
                    "Pickaxe Power": "",
                    "Hammer Power": "",
                    "Axe Power": "",
                    "Fishing Power": "",
                    "Recipes": [] 
                }
                jsonDict["Item ID"] = item["ID"]
                jsonDict["Name"] = item["Name"]

                rarity = table.find("span", class_="rarity")
                if rarity:
                    jsonDict["Rarity"] = rarity.a["title"][-1]

                use_time = table.find("span", class_="usetime")
                if use_time:
                    use_time = use_time.parent
                    jsonDict["Use Time"] = use_time.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()

                tool_speed = table.find("a", title="Mining speed")
                if tool_speed:
                    tool_speed = tool_speed.parent.parent.find("td")
                    jsonDict["Tool Speed"] = tool_speed.text.split(" ", 1)[0]

                power = table.find("ul", class_="toolpower")
                if power:
                    powerList = power.find_all("li")
                    for powerType in powerList:
                        if(powerType["title"] == "Pickaxe power"):
                            jsonDict["Pickaxe Power"] = powerType.text[1:].split(" ", 1)[0]
                        elif(powerType["title"] == "Hammer power"):
                            jsonDict["Hammer Power"] = powerType.text[1:].split(" ", 1)[0]
                        elif(powerType["title"] == "Axe power"):
                            jsonDict["Axe Power"] = powerType.text[1:].split(" ", 1)[0]

                jsonDict["Recipes"] = []
                jsonList.append(jsonDict)
        else:
            trTags = soup.find("table", id="fishing-poles-table").find_all("tr")
            for trTag in trTags[1:]:
                tdTags = trTag.find_all("td")
                if tdTags[1].span.span.span.text == item["Name"]:
                    jsonDict = {
                        "Item ID": "",
                        "Name": "",
                        "Rarity": "",
                        "Use Time": "",
                        "Velocity": "",
                        "Tool Speed": "",
                        "Pickaxe Power": "",
                        "Hammer Power": "",
                        "Axe Power": "",
                        "Fishing Power": "",
                        "Recipes": [] 
                    }
                    jsonDict["Item ID"] = item["ID"]
                    jsonDict["Name"] = item["Name"]
                    jsonDict["Fishing Power"] = tdTags[3].text.rstrip()
                    jsonDict["Velocity"] = tdTags[4].text.rstrip()
                    jsonDict["Rarity"] = tdTags[6].a["title"][-1]
                    jsonList.append(jsonDict)
                    break

SaveJSONFile(ITEM_PATH_OUTPUT, jsonList)