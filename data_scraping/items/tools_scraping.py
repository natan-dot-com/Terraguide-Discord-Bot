#fishing poles aren't being processed

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
import requests
from bs4 import BeautifulSoup

item_path_output = GLOBAL_JSON_PATH + "items_tools.json"

item_list = LoadJSONFile(ITEM_FILE_PATH)
url = "https://terraria.gamepedia.com/"
json_list = []

for item in item_list:
    if item["type"] == "Tool":
        new_url = url + item["name"].replace(" ", "_")
        page = requests.get(new_url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("div", class_="infobox item")

        if table:
            json_dict = {
                "Item ID": "",
                "Name": "",
                "Rarity": "",
                "Use Time": "",
                "Tool Speed": "",
                "Pickaxe Power": "",
                "Hammer Power": "",
                "Axe Power": "",
                "Recipes": [] 
            }
            json_dict["Item ID"] = item["id"]
            json_dict["Name"] = item["name"]

            rarity = table.find("span", class_="rarity")
            if rarity:
                json_dict["Rarity"] = rarity.a["title"][-1]

            use_time = table.find("span", class_="usetime")
            if use_time:
                use_time = use_time.parent
                json_dict["Use Time"] = use_time.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()

            tool_speed = table.find("a", title="Mining speed")
            if tool_speed:
                tool_speed = tool_speed.parent.parent.find("td")
                json_dict["Tool Speed"] = tool_speed.text.split(" ", 1)[0]

            power = table.find("ul", class_="toolpower")
            if power:
                powerList = power.find_all("li")
                for powerType in powerList:
                    if(powerType["title"] == "Pickaxe power"):
                        json_dict["Pickaxe Power"] = powerType.text[1:].split(" ", 1)[0]
                    elif(powerType["title"] == "Hammer power"):
                        json_dict["Hammer Power"] = powerType.text[1:].split(" ", 1)[0]
                    elif(powerType["title"] == "Axe power"):
                        json_dict["Axe Power"] = powerType.text[1:].split(" ", 1)[0]

            json_dict["Recipes"] = []
            json_list.append(json_dict)

SaveJSONFile(item_path_output, json_list)