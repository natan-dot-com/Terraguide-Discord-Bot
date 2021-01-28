
#Everything seems to work.

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
import requests
from bs4 import BeautifulSoup

ITEM_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_weapons.json"
ITEM_URL = ["Enchanted Sword"]

itemList = LoadJSONFile(ITEM_FILE_PATH)
url = "https://terraria.gamepedia.com/"
jsonList = []

for itemInstance in itemList:
    if itemInstance["Type"] == "Weapon":
        newURL = url + itemInstance["Name"].replace(" ", "_")
        if itemInstance["Name"] in ITEM_URL:
            newURL += "_(item)"
        print("Processing " + newURL + " with ID " + itemInstance["ID"])
        page = requests.get(newURL)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("div", class_="infobox item")

        if table:
            jsonDict = {
                "Item ID": "",
                "Name": "",
                "Damage": "",
                "Knockback": "",
                "Mana": "",
                "Critical Chance": "",
                "Use Time": "",
                "Velocity": "",
                "Rarity": "",
                "Research": "",
                "Recipes": [] 
            }
            jsonDict["Item ID"] = itemInstance["ID"]
            jsonDict["Name"] = itemInstance["Name"]

            damage = table.find("th", text="Damage")
            if damage:
                jsonDict["Damage"] = damage.parent.td.text.split(" ")[0]

            knockback = table.find("span", class_="knockback")
            if knockback:
                jsonDict["Knockback"] = knockback.parent.text.split("/")[0].rstrip()

            mana = table.find("a", title="Mana")
            if mana:
                jsonDict["Mana"] = mana.parent.parent.td.text.split(" ")[0]

            critical_chance = table.find("a", title="Critical hit")
            if critical_chance:
                jsonDict["Critical Chance"] = critical_chance.parent.parent.td.text.split(" ")[0]

            use_time = table.find("span", class_="usetime")
            if use_time:
                use_time = use_time.parent
                jsonDict["Use Time"] = use_time.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()

            velocity = table.find("a", title="Velocity")
            if velocity:
                jsonDict["Velocity"] = velocity.parent.parent.td.text.split(" ")[0]

            rarity = table.find("span", class_="rarity")
            if rarity:
                jsonDict["Rarity"] = rarity.a["title"][-1]

            research = table.find("a", title="Journey mode")
            if research:
                jsonDict["Research"] = research.parent.parent.td.text

            jsonDict["Recipes"] = []
            jsonList.append(jsonDict)

SaveJSONFile(ITEM_PATH_OUTPUT, jsonList)
