#Need to improve coding but everything works probably

import os,sys,inspect
import re
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from scraping_tools import *
from json_manager import *
import requests
from bs4 import BeautifulSoup

def get_statistics(tableBox, usedIn):
    ammoDict = {
        SCRAPING_ITEM_ID: "",
        SCRAPING_NAME: "",
        SCRAPING_USED_IN: "",
        SCRAPING_DAMAGE: "",
        SCRAPING_VELOCITY: "",
        SCRAPING_MULTIPLIER: "",
        SCRAPING_KNOCKBACK: "",
        SCRAPING_AVAILABLE: "",
        SCRAPING_AVAILABILITY: "",
        SCRAPING_EFFECT: "",
        SCRAPING_SOURCE: "",
        SCRAPING_RADIUS: "",
        SCRAPING_DESTROY_TILES: "",
        SCRAPING_RARITY: "",
        SCRAPING_TOOLTIP: "",
        SCRAPING_SOURCES: SOURCE_SOURCES_DICT
    }

    ammoDict[SCRAPING_ITEM_ID] = tableBox.find("div", class_="section ids").find("li").b.text
    ammoDict[SCRAPING_NAME] = tableBox.find("div", class_="title").text
    if usedIn:
        ammoDict[SCRAPING_USED_IN] = usedIn
    statistics = tableBox.find("div", class_="section statistics").find_all("tr")
    for statistic in statistics:
        if statistic.th.text == SCRAPING_DAMAGE:
            ammoDict[SCRAPING_DAMAGE] = statistic.td.text.split(' ')[0].rstrip()
        elif statistic.th.text == SCRAPING_VELOCITY:
            ammoDict[SCRAPING_VELOCITY] = statistic.td.text.split(' ')[0].rstrip()
        elif statistic.th.text == SCRAPING_KNOCKBACK:
            ammoDict[SCRAPING_KNOCKBACK] = statistic.td.text.rstrip()
        elif statistic.th.text == SCRAPING_AVAILABLE:
            ammoDict[SCRAPING_AVAILABLE] = (statistic.td.text.rstrip()).replace("  ", " ")
        elif statistic.th.text == SCRAPING_EFFECT:
            ammoDict[SCRAPING_EFFECT] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
        elif statistic.th.text == SCRAPING_RARITY:
            ammoDict[SCRAPING_RARITY] = (re.search("-*\d+", statistic.td.span.a["title"])).group()
        elif statistic.th.text == SCRAPING_TOOLTIP:
            ammoDict[SCRAPING_TOOLTIP] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
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
                SCRAPING_ITEM_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_USED_IN: "",
                SCRAPING_DAMAGE: "",
                SCRAPING_VELOCITY: "",
                SCRAPING_MULTIPLIER: "",
                SCRAPING_KNOCKBACK: "",
                SCRAPING_AVAILABLE: "",
                SCRAPING_AVAILABILITY: "",
                SCRAPING_EFFECT: "",
                SCRAPING_SOURCE: "",
                SCRAPING_RADIUS: "",
                SCRAPING_DESTROY_TILES: "",
                SCRAPING_RARITY: "",
                SCRAPING_TOOLTIP: "",
                SCRAPING_SOURCES: SOURCE_SOURCES_DICT
            }
            tdTags = item.find_all("td")

            id = item.find("div", class_="id")      
            ammoDict[SCRAPING_ITEM_ID] = (re.search("\d+", id.text)).group()
            ammoDict[SCRAPING_NAME] = item.img['alt']
            if pageName == "Arrows":
                ammoDict[SCRAPING_USED_IN] = "Any Bow or Repeater."
            elif pageName == "Bullets":
                ammoDict[SCRAPING_USED_IN] = "Any Gun"
            elif pageName == "Darts":
                ammoDict[SCRAPING_USED_IN] = "Blowgun, Blowpipe, Dart Pistol and Dart Rifle"
            ammoDict[SCRAPING_DAMAGE] = tdTags[2].text.split(' ')[0].rstrip()
            if tdTags[3].text.split(' ')[0] != "???\n":
                ammoDict[SCRAPING_VELOCITY] = tdTags[3].text.split(' ')[0].rstrip()
            ammoDict[SCRAPING_MULTIPLIER] = tdTags[4].text.split(' ')[0].rstrip()
            if tdTags[5].text != "???\n":
                ammoDict[SCRAPING_KNOCKBACK] = " (".join(tdTags[5].text.rstrip().split("("))
            ammoDict[SCRAPING_RARITY] = tdTags[7].a['title'].split(' ')[-1]
            ammoList.append(ammoDict)

    #for Rockets page
    elif pageName == "Rockets":

        items = soup.find("table", class_="terraria").find_all("tr")

        for item in items[1:]:
            if item.find_all("td")[0].find("img", alt=OTHER_VERSIONS) and not item.find_all("td")[1].find("img", alt=DESKTOP_VERSION):
                print("item {} isn't desktop".format(item.img['alt']))
                continue

            ammoDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_USED_IN: "",
                SCRAPING_DAMAGE: "",
                SCRAPING_VELOCITY: "",
                SCRAPING_MULTIPLIER: "",
                SCRAPING_KNOCKBACK: "",
                SCRAPING_AVAILABLE: "",
                SCRAPING_AVAILABILITY: "",
                SCRAPING_EFFECT: "",
                SCRAPING_SOURCE: "",
                SCRAPING_RADIUS: "",
                SCRAPING_DESTROY_TILES: "",
                SCRAPING_RARITY: "",
                SCRAPING_TOOLTIP: "",
                SCRAPING_SOURCES: SOURCE_SOURCES_DICT
            }
            tdTags = item.find_all("td")

            id = item.find("div", class_="id")      
            ammoDict[SCRAPING_ITEM_ID] = (re.search("\d+", id.text)).group()
            ammoDict[SCRAPING_NAME] = item.img['alt']
            ammoDict['Used In'] = "Launcher"
            ammoDict[SCRAPING_DAMAGE] = tdTags[1].text.split(' ')[0].rstrip()
            ammoDict[SCRAPING_AVAILABILITY] = tdTags[2].text.rstrip().replace("or", "or ")
            ammoDict[SCRAPING_RARITY] = tdTags[3].a['title'].split(' ')[-1]
            if not tdTags[2].find("img"):
                ammoDict[SCRAPING_SOURCE] = tdTags[4].text.split('(')[0].rstrip()
            ammoDict[SCRAPING_RADIUS] = tdTags[5].text.rstrip()
            ammoDict[SCRAPING_DESTROY_TILES] = tdTags[6].img['alt']
            ammoList.append(ammoDict)

    #for Solutions page
    elif pageName == "Solutions":

        items = soup.find("table", class_="terraria").find_all("tr")

        for item in items[1:]:
            if item.find_all("td")[0].find("img", alt=OTHER_VERSIONS) and not item.find_all("td")[1].find("img", alt=DESKTOP_VERSION):
                print("item {} isn't desktop".format(item.img['alt']))
                continue

            ammoDict = {
                SCRAPING_ITEM_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_USED_IN: "",
                SCRAPING_DAMAGE: "",
                SCRAPING_VELOCITY: "",
                SCRAPING_MULTIPLIER: "",
                SCRAPING_KNOCKBACK: "",
                SCRAPING_AVAILABLE: "",
                SCRAPING_AVAILABILITY: "",
                SCRAPING_EFFECT: "",
                SCRAPING_SOURCE: "",
                SCRAPING_RADIUS: "",
                SCRAPING_DESTROY_TILES: "",
                SCRAPING_RARITY: "",
                SCRAPING_TOOLTIP: "",
                SCRAPING_SOURCES: SOURCE_SOURCES_DICT
            }
            tdTags = item.find_all("td")
            id = item.find("div", class_="id")      
            ammoDict[SCRAPING_ITEM_ID] = (re.search("\d+", id.text)).group()
            ammoDict[SCRAPING_NAME] = item.img['alt']
            ammoDict[SCRAPING_AVAILABLE] = " ".join((tdTags[1].text.rstrip()).split("  "))
            ammoDict[SCRAPING_EFFECT] = BeautifulSoup(str(tdTags[2]).replace("<br/>", ". "), 'html.parser').text.rstrip()
            ammoDict[SCRAPING_RARITY] = "3"
            ammoDict[SCRAPING_TOOLTIP] = BeautifulSoup(str(tdTags[3]).replace("<br/>", ". "), 'html.parser').text.rstrip()
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
                SCRAPING_ITEM_ID: "",
                SCRAPING_NAME: "",
                SCRAPING_USED_IN: "",
                SCRAPING_DAMAGE: "",
                SCRAPING_VELOCITY: "",
                SCRAPING_MULTIPLIER: "",
                SCRAPING_KNOCKBACK: "",
                SCRAPING_AVAILABLE: "",
                SCRAPING_AVAILABILITY: "",
                SCRAPING_EFFECT: "",
                SCRAPING_SOURCE: "",
                SCRAPING_RADIUS: "",
                SCRAPING_DESTROY_TILES: "",
                SCRAPING_RARITY: "",
                SCRAPING_TOOLTIP: "",
                SCRAPING_SOURCES: SOURCE_SOURCES_DICT
            }
            id = tableCoin.find("div", class_="id")
            tdTags = tableCoin.find_all("td")
            ammoDict[SCRAPING_ITEM_ID] = (re.search("\d+", id.text)).group()
            ammoDict[SCRAPING_NAME] = tdTags[1].span.span.span.text
            ammoDict[SCRAPING_USED_IN] = "Coin Gun"
            ammoDict[SCRAPING_DAMAGE] = tdTags[4].text.rstrip()
            ammoDict[SCRAPING_VELOCITY] = tdTags[5].text.rstrip()
            ammoDict[SCRAPING_RARITY] = soup.find("div", class_="infobox item").find("span", class_="rarity").a['title'].split(' ')[-1]
            ammoList.append(ammoDict)

    elif ammo == "Flare":
        tableBoxes = soup.find_all("div", class_="infobox item")
        for tableBox in tableBoxes[1:]:       
            ammoList.append(get_statistics(tableBox, "Flare Gun"))

    else:
        tableBox = soup.find("div", class_="infobox item")
        ammoList.append(get_statistics(tableBox, ""))

SaveJSONFile(AMMO_PATH_OUTPUT, ammoList)
