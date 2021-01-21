
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
import json
from tools import *
import requests
from bs4 import BeautifulSoup

item_path = 'json_new/items.json'
item_path_output = 'json_new/items_weapons.json'

item_list = LoadJSONFile(item_path)
url = "https://terraria.gamepedia.com/"
json_list = []

for item in item_list:
    if item['type'] == "Weapon":
        print(item['name'], item['id'])
        new_url = url + item['name'].replace(" ", "_")
        page = requests.get(new_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find("div", class_="infobox item")

        if table:
            json_dict = {
                "id": "",
                "name": "",
                "Damage": "",
                "Knockback": "",
                "Mana": "",
                "Critical Chance": "",
                "Use Time": "",
                "Velocity": "",
                "Rarity": "",
                "Research": "",
                "recipes": [] 
            }
            json_dict['id'] = item['id']
            json_dict['name'] = item['name']

            damage = table.find("th", text="Damage")
            if damage:
                json_dict['Damage'] = damage.parent.td.text.split(' ')[0]

            knockback = table.find("span", class_="knockback")
            if knockback:
                json_dict['Knockback'] = knockback.parent.text.split('/')[0].rstrip()

            mana = table.find("a", title="Mana")
            if mana:
                json_dict['Mana'] = mana.parent.parent.td.text.split(' ')[0]

            critical_chance = table.find("a", title="Critical hit")
            if critical_chance:
                json_dict['Critical Chance'] = critical_chance.parent.parent.td.text.split(' ')[0]

            use_time = table.find("span", class_="usetime")
            if use_time:
                use_time = use_time.parent
                json_dict['Use Time'] = use_time.text.split('/')[0].encode("ascii", "ignore").decode().rstrip()

            velocity = table.find("a", title="Velocity")
            if velocity:
                json_dict['Velocity'] = velocity.parent.parent.td.text.split(' ')[0]

            rarity = table.find("span", class_="rarity")
            if rarity:
                json_dict['Rarity'] = rarity.a['title'][-1]

            research = table.find("a", title="Journey mode")
            if research:
                json_dict['Research'] = research.parent.parent.td.text

            json_dict['recipes'] = []
            json_list.append(json_dict)

SaveJSONFile(item_path_output, json_list)
