#Need to improve coding but everything works probably

import os,sys,inspect
import re
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *
import requests
from bs4 import BeautifulSoup

def get_statistics(tableBox, usedIn):
    ammoDict = {
        "Item ID": "",
        "Name": "",
        "Used In": "",
        "Damage": "",
        "Velocity": "",
        "Multiplier": "",
        "Knockback": "",
        "Available": "",
        "Availability": "",
        "Effect": "",
        "Source": "",
        "Radius": "",
        "Destroy Tiles": "",
        "Rarity": "",
        "Tooltip": "",
        "Recipes": []
    }

    ammoDict["Item ID"] = tableBox.find("div", class_="section ids").find("li").b.text
    ammoDict["Name"] = tableBox.find("div", class_="title").text
    if usedIn:
        ammoDict["Used In"] = usedIn
    statistics = tableBox.find("div", class_="section statistics").find_all("tr")
    for statistic in statistics:
        if statistic.th.text == "Damage":
            ammoDict["Damage"] = statistic.td.text.split(' ')[0].rstrip()
        elif statistic.th.text == "Velocity":
            ammoDict["Velocity"] = statistic.td.text.split(' ')[0].rstrip()
        elif statistic.th.text == "Knockback":
            ammoDict["Knockback"] = statistic.td.text.rstrip()
        elif statistic.th.text == "Available":
            ammoDict["Available"] = (statistic.td.text.rstrip()).replace("  ", " ")
        elif statistic.th.text == "Effect":
            ammoDict["Effect"] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
        elif statistic.th.text == "Rarity":
            ammoDict["Rarity"] = statistic.td.span.a["title"][-1]
        elif statistic.th.text == "Tooltip":
            ammoDict["Tooltip"] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
    return ammoDict

OTHER_VERSIONS = {"3DS version", "Console Version", "Old-gen console version", "Mobile version"}
DESKTOP_VERSION = {"Desktop"}
AMMO_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_ammos.json"
AMMOS_TYPES = ["Arrows", "Bullets", "Rockets", "Darts", "Solutions"]
AMMO_EXCEPTIONS = [
    "Gel", "Coins", "Fallen Star", "Seed", "Cannonball", "Snowball", "Stynger Bolt", "Explosive Bunny",
    "Confetti", "Candy Corn", "Explosive Jack 'O Lantern", "Stake", "Nail", "Flare"
]

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
            if item.find_all("td")[1].find("img", alt=OTHER_VERSIONS) and not item.find_all("td")[1].find("img", alt=DESKTOP_VERSION):
                print("item {} isn't desktop".format(item.img['alt']))
                continue

            ammoDict = {
                "Item ID": "",
                "Name": "",
                "Used In": "",
                "Damage": "",
                "Velocity": "",
                "Multiplier": "",
                "Knockback": "",
                "Available": "",
                "Availability": "",
                "Effect": "",
                "Source": "",
                "Radius": "",
                "Destroy Tiles": "",
                "Rarity": "",
                "Tooltip": "",
                "Recipes": [] 
            }
            tdTags = item.find_all("td")

            id = item.find("div", class_="id")      
            ammoDict["Item ID"] = (re.search("\d+", id.text)).group()
            ammoDict["Name"] = item.img['alt']
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
            ammoList.append(ammoDict)

    #for Rockets page
    elif pageName == "Rockets":

        items = soup.find("table", class_="terraria").find_all("tr")

        for item in items[1:]:
            if item.find_all("td")[0].find("img", alt=OTHER_VERSIONS) and not item.find_all("td")[1].find("img", alt=DESKTOP_VERSION):
                print("item {} isn't desktop".format(item.img['alt']))
                continue

            ammoDict = {
                "Item ID": "",
                "Name": "",
                "Used In": "",
                "Damage": "",
                "Velocity": "",
                "Multiplier": "",
                "Knockback": "",
                "Available": "",
                "Availability": "",
                "Effect": "",
                "Source": "",
                "Radius": "",
                "Destroy Tiles": "",
                "Rarity": "",
                "Tooltip": "",
                "Recipes": []
            }
            tdTags = item.find_all("td")

            id = item.find("div", class_="id")      
            ammoDict["Item ID"] = (re.search("\d+", id.text)).group()
            ammoDict["Name"] = item.img['alt']
            ammoDict['Used in'] = "Launcher"
            ammoDict["Damage"] = tdTags[1].text.split(' ')[0].rstrip()
            ammoDict["Availability"] = tdTags[2].text.rstrip().replace("or", "or ")
            ammoDict["Rarity"] = tdTags[3].a['title'].split(' ')[-1]
            if not tdTags[2].find("img"):
                ammoDict["Source"] = tdTags[4].text.split('(')[0].rstrip()
            ammoDict["Radius"] = tdTags[5].text.rstrip()
            ammoDict["Destroy Tiles"] = tdTags[6].img['alt']
            ammoList.append(ammoDict)

    #for Solutions page
    elif pageName == "Solutions":

        items = soup.find("table", class_="terraria").find_all("tr")

        for item in items[1:]:
            if item.find_all("td")[0].find("img", alt=OTHER_VERSIONS) and not item.find_all("td")[1].find("img", alt=DESKTOP_VERSION):
                print("item {} isn't desktop".format(item.img['alt']))
                continue

            ammoDict = {
                "Item ID": "",
                "Name": "",
                "Used In": "",
                "Damage": "",
                "Velocity": "",
                "Multiplier": "",
                "Knockback": "",
                "Available": "",
                "Availability": "",
                "Effect": "",
                "Source": "",
                "Radius": "",
                "Destroy Tiles": "",
                "Rarity": "",
                "Tooltip": "",
                "Recipes": []
            }
            tdTags = item.find_all("td")
            id = item.find("div", class_="id")      
            ammoDict["Item ID"] = (re.search("\d+", id.text)).group()
            ammoDict["Name"] = item.img['alt']
            ammoDict["Available"] = " ".join((tdTags[1].text.rstrip()).split("  "))
            ammoDict["Effect"] = BeautifulSoup(str(tdTags[2]).replace("<br/>", ". "), 'html.parser').text.rstrip()
            ammoDict["Rarity"] = "3"
            ammoDict["Tooltip"] = BeautifulSoup(str(tdTags[3]).replace("<br/>", ". "), 'html.parser').text.rstrip()
            ammoList.append(ammoDict)


for ammo in AMMO_EXCEPTIONS:
    print("Processing {}".format(ammo))
    newURL = wikiURL + ammo
    page = requests.get(newURL)
    soup = BeautifulSoup(page.content, 'html.parser')

    if ammo == "Coins":
        tableCoins = soup.find("table", class_="terraria").tbody.find_all("tr")
        for tableCoin in tableCoins[1:]:
            ammoDict = {
                "Item ID": "",
                "Name": "",
                "Used In": "",
                "Damage": "",
                "Velocity": "",
                "Multiplier": "",
                "Knockback": "",
                "Available": "",
                "Availability": "",
                "Effect": "",
                "Source": "",
                "Radius": "",
                "Destroy Tiles": "",
                "Rarity": "",
                "Tooltip": "",
                "Recipes": []
            }
            id = tableCoin.find("div", class_="id")
            tdTags = tableCoin.find_all("td")
            ammoDict["Item ID"] = (re.search("\d+", id.text)).group()
            ammoDict["Name"] = tdTags[1].span.span.span.text
            ammoDict["Used In"] = "Coin Gun"
            ammoDict["Damage"] = tdTags[4].text.rstrip()
            ammoDict["Velocity"] = tdTags[5].text.rstrip()
            ammoDict["Rarity"] = soup.find("div", class_="infobox item").find("span", class_="rarity").a['title'].split(' ')[-1]
            ammoList.append(ammoDict)

    elif ammo == "Flare":
        tableBoxes = soup.find_all("div", class_="infobox item")
        for tableBox in tableBoxes[1:]:       
            ammoList.append(get_statistics(tableBox, "Flare Gun"))

    else:
        tableBox = soup.find("div", class_="infobox item")
        ammoList.append(get_statistics(tableBox, ""))

SaveJSONFile(AMMO_PATH_OUTPUT, ammoList)
