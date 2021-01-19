import json
from json_manager import *
from tools import *
import requests
from bs4 import BeautifulSoup

itemList = LoadJSONFile('json_new/items.json')
url = "https://terraria.gamepedia.com/"

#First you need to generate a blank json
'''json_dict = {
    "id": "",
    "name": "",
    "Rarity": "",
    "Use Time": "",
    "Tool Speed": "",
    "Pickaxe Power": "",
    "Hammer Power": "",
    "Axe Power": "",
    "recipes": [] 
}
json_list = []


for item in itemList:
    if item['type'] == "Tool":
        json_list.append(json_dict)
with open('json_new/items_tools.json', "w") as output:
    json.dump(json_list, output, indent=2)
exit(0)'''

counter = 0

with open('json_new/items_tools.json', "r+") as json_file:
    json_list = json.load(json_file)

    for item in itemList:
        if item['type'] == "Tool":
            #print(item['name'] + item['id'])
            new_url = url + item['name'].replace(" ", "_")
            page = requests.get(new_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            table = soup.find("div", class_="infobox item")

            if table:
                json_list[counter]['id'] = item['id']
                json_list[counter]['name'] = item['name']

                rarity = table.find("span", class_="rarity")
                if rarity:
                    json_list[counter]['Rarity'] = rarity.a['title'][-1]

                use_time = table.find("span", class_="usetime")
                if use_time:
                    use_time = use_time.parent
                    json_list[counter]['Use Time'] = use_time.text

                tool_speed = table.find("a", title="Mining speed")
                if tool_speed:
                    tool_speed = tool_speed.parent.parent.find("td")
                    json_list[counter]['Tool Speed'] = tool_speed.text.split(' ', 1)[0]

                power = table.find("ul", class_="toolpower")
                if power:
                    powerList = power.find_all("li")
                    for powerType in powerList:
                        if(powerType['title'] == "Pickaxe power"):
                            json_list[counter]['Pickaxe Power'] = powerType.text[1:].split(' ', 1)[0]
                        elif(powerType['title'] == "Hammer power"):
                            json_list[counter]['Hammer Power'] = powerType.text[1:].split(' ', 1)[0]
                        elif(powerType['title'] == "Axe power"):
                            json_list[counter]['Axe Power'] = powerType.text[1:].split(' ', 1)[0]

                json_list[counter]['recipes'] = []
                counter += 1

    json_file.seek(0)
    json.dump(json_list, json_file, indent=2)