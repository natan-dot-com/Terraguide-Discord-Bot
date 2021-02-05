import requests
import re
from bs4 import BeautifulSoup
import operator

# General labels
SCRAPING_ID = "ID"
SCRAPING_TYPE = "Type"
SCRAPING_ITEM_ID = "Item ID"
SCRAPING_NAME = "Name"
SCRAPING_RARITY = "Rarity"
SCRAPING_USE_TIME = "Use time"
SCRAPING_VELOCITY = "Velocity"
SCRAPING_TOOL_SPEED = "Tool speed"
SCRAPING_PICKAXE_POWER = "Pickaxe power"
SCRAPING_HAMMER_POWER = "Hammer power"
SCRAPING_AXE_POWER = "Axe power"
SCRAPING_FISHING_POWER = "Fishing Power"
SCRAPING_SET_ID = "Set ID"
SCRAPING_DEFENSE = "Defense"
SCRAPING_BODY_SLOT = "Body slot"
SCRAPING_TOOLTIP = "Tooltip"
SCRAPING_RESEARCH = "Research"
SCRAPING_USED_IN = "Used In"
SCRAPING_DAMAGE = "Damage"
SCRAPING_MULTIPLIER = "Multiplier"
SCRAPING_KNOCKBACK = "Knockback"
SCRAPING_AVAILABLE = "Available"
SCRAPING_AVAILABILITY = "Availability"
SCRAPING_EFFECT = "Effect"
SCRAPING_SOURCE = "Source"
SCRAPING_RADIUS = "Radius"
SCRAPING_DESTROY_TILES = "Destroy Tiles"
SCRAPING_PLACEABLE = "Placeable"
SCRAPING_SET_PIECES = "Set Pieces"
SCRAPING_SET_NAME = "Set Name"
SCRAPING_SET_BONUS = "Set Bonus"
SCRAPING_MANA = "Mana"
SCRAPING_CRITICAL_CHANCE = "Critical chance"
SCRAPING_REACH = "Reach"
SCRAPING_HOOKS = "Hooks"
SCRAPING_LATCHING = "Latching"
SCRAPING_IN_STONE = "In Stone"
SCRAPING_PLACED = "Placed"
SCRAPING_ORE_TIER = "Ore Tier"
SCRAPING_MINIMUM_PICKAXE_POWER = "Minimum Pickaxe Power"
SCRAPING_CONSUMED = "Is Consumed"
SOURCE_RECIPES = "Crafting Recipes"
SCRAPING_ANGLER_QUOTE = "Angler Quote"
SCRAPING_HEIGHT = "Height"
SCRAPING_BIOME = "Biome"
SCRAPING_SOURCES = "Sources"
SCRAPING_RARITY_ID = "Rarity ID"
SCRAPING_RARITY_TIER = "Rarity Tier"
SCRAPING_IMAGE_PATH = "Image Path"
SCRAPING_RARITY_DESC = "Rarity Description"
SCRAPING_MAX_LIFE = "Max Life"
SCRAPING_BUY = "Buy"
SCRAPING_SELL = "Sell"
SCRAPING_BASE_VELOCITY = "Base Velocity"
SCRAPING_VELOCITY_MULTIPLIER = "Velocity Multiplier"
SCRAPING_LIGHT_PET = "Light Pet"
SCRAPING_BRIGHTNESS = "Brightness"
SCRAPING_NOTES = "Notes"
SCRAPING_BUFF_IMAGE = "Buff Image"
SCRAPING_PET_IMAGE = "Light Pet Image"
SCRAPING_MASTER_MODE = "Master Mode Exclusive:"
SCRAPING_DESCRIPTION = "Description"
SCRAPING_TOOLTIP = "Tooltip"
SCRAPING_DESTROYED_BY_EXPLOSIVES = "Destroyed by Explosives"
SCRAPING_BONUS = "Bonus"
SCRAPING_USABLE = "Usable"
SCRAPING_MAX_STACK = "Max stack"
SCRAPING_CREATES = "Creates"
SCRAPING_PLANTED_IN = "Planted In"
SCRAPING_CATCH_QUALITY = "Catch Quality"
SCRAPING_EVENT = "Event"
SCRAPING_BAIT_POWER = "Bait Power"
SCRAPING_SUMMONS = "Summons"
SCRAPING_HOUSE = "House"
SCRAPING_MECHANISM = "Mechanism"
SCRAPING_WATERPROOF = "Waterproof"

# Source dict labels ('SCRAPING_SOURCE')
SOURCE_RECIPE = "Crafting Recipes"
SOURCE_NPC = "NPC"
SOURCE_DROP = "Drop"
SOURCE_GRAB_BAG = "Grab Bag"
SOURCE_OTHER = "Other"
SOURCE_SOURCES_DICT = {
    SOURCE_RECIPES: [],
    SOURCE_NPC: [],
    SOURCE_DROP: [],
    SOURCE_GRAB_BAG: [],
    SOURCE_OTHER: "",
}

# Drop dict labels ('SCRAPING_SOURCE' subdict)
DROP_ID = "Drop ID"
DROP_NPC = "NPC"
DROP_PROBABILITY = "Probability"
DROP_QUANTITY = "Quantity"
DROP_DROPS_DICT = {
    DROP_ID: "",
    DROP_NPC: "",
    DROP_PROBABILITY: "",
    DROP_QUANTITY: ""
}

# Crafting recipe labels ('SCRAPING_SOURCE' subdict)
RECIPE_CRAFT_ID = "Craft ID"
RECIPE_RESULT = "Result ID"
RECIPE_RESULT_QUANTITY = "Result Quantity"
RECIPE_TABLE = "Table ID"
RECIPE_IDENTITY = "Recipe"
RECIPE_CRAFTING_DICT = {
    RECIPE_CRAFT_ID: "",
    RECIPE_RESULT: "",
    RECIPE_RESULT_QUANTITY: "",
    RECIPE_TABLE: "",
    RECIPE_IDENTITY: []
}

# Recipe ingredient labels ('RECIPE_IDENTITY' subdict)
INGREDIENT_NAME = "Ingredient ID"
INGREDIENT_QUANTITY = "Quantity"
INGREDIENT_DICT = {
    INGREDIENT_NAME: "",
    INGREDIENT_QUANTITY: ""
}

# Grab bag dict labels ('SCRAPING_SOURCE' subdict)
BAG_DROP_ID = "Bag Drop ID"
BAG_ID = "Bag ID"
BAG_DROP_PROBABILITY = "Probability"
BAG_DROP_QUANTITY = "Quantity"
BAG_DROPS_DICT = {
    BAG_DROP_ID: "",
    BAG_ID: "",
    BAG_DROP_PROBABILITY: "",
    BAG_DROP_QUANTITY: ""
}

RARITY_GRAY = "Gray"
RARITY_AMBER = "Quest"
RARITY_RAINBOW = "Rainbow"
RARITY_FIERY_RED = "Fiery red"
RARITY_TIER = {
    RARITY_GRAY: "-1",
    RARITY_AMBER: "-11",
    RARITY_RAINBOW: "-12",
    RARITY_FIERY_RED: "-13"
}

BOSS_SUMMON_JSON_NAME_FILE = "items_boss_summons.json"
LIGHT_SOURCE_JSON_NAME_FILE = "light_sources.json"

NOT_FOUND = -1
FOUND = 1

# Find the ID in respect of an item in items.json
def searchForID(itemName, itemList):
    for itemInstance in itemList:
        if itemName == itemInstance[SCRAPING_NAME]:
            return itemInstance[SCRAPING_ID]

# Write/saves an image from a HTML scrap
def writeImage(imageSource, imagePath):
    imgOutput = requests.get(imageSource, stream=True)
    if imgOutput.ok:
        with open(imagePath, "wb+") as handler:
            for block in imgOutput.iter_content(1024):
                if not block:
                    break
                handler.write(block)
    else:
        return NOT_FOUND
    return FOUND

# Removes every null field inside a dict
def removeEmptyFields(dataDict):
    dictEmptyKeys = []
    for key in dataDict.keys():
        if dataDict[key] == "":
            dictEmptyKeys.append(key)
    for key in dictEmptyKeys:
        del(dataDict[key])
    return dataDict

def sortListOfDictsByKey(dataList, key):
    return sorted(dataList, key=lambda x: int(operator.itemgetter(key)(x)))
    
# Finds every column index of a table based on a list with each column label. 
def getTableColumns(tableHeadRow, scrappingData):
    indexDict = {}
    for data in scrappingData:
        indexDict[data] = NOT_FOUND
        for column in tableHeadRow:
            if re.search("^" + data, column.text):
                indexDict[data] = int(tableHeadRow.index(column))
    return indexDict

#get statistics for every table with infobox class
def get_statistics(tableBox, itemInstance = {}, usedIn = "", isArmor = False):

    jsonDict = {}
    #Check if optional parameter was given
    if itemInstance:
        jsonDict[SCRAPING_ITEM_ID] = itemInstance[SCRAPING_ID]
        jsonDict[SCRAPING_NAME] = itemInstance[SCRAPING_NAME]
    else:
        jsonDict[SCRAPING_ITEM_ID] = tableBox.find("div", class_="section ids").find("li").b.text
        jsonDict[SCRAPING_NAME] = tableBox.find("div", class_="title").text

    statistics = tableBox.find("div", class_="section statistics").find_all("tr")
    for statistic in statistics:
        if statistic.th.text == SCRAPING_USE_TIME:
            jsonDict[SCRAPING_USE_TIME] = statistic.td.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()
        elif statistic.th.text == SCRAPING_RARITY:
            if statistic.td.span:
                if (re.search("-*\d+", statistic.td.span.a["title"])):
                    jsonDict[SCRAPING_RARITY] = (re.search("-*\d+", statistic.td.span.a["title"])).group()
                else:
                    jsonDict[SCRAPING_RARITY] = RARITY_TIER[statistic.td.span.a["title"].split(": ")[-1]]
            else:
                jsonDict[SCRAPING_RARITY] = statistic.td.text.rstrip()
        elif statistic.th.text == SCRAPING_PLACEABLE:
            jsonDict[SCRAPING_PLACEABLE] = statistic.td.img["alt"]
        elif statistic.th.text == SCRAPING_MAX_LIFE:
            jsonDict[SCRAPING_MAX_LIFE] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
        elif statistic.th.text == SCRAPING_RESEARCH:
            jsonDict[SCRAPING_RESEARCH] = statistic.td.text.rstrip()
        elif statistic.th.text == SCRAPING_TOOL_SPEED:
            jsonDict[SCRAPING_TOOL_SPEED] = statistic.td.text.split(" ", 1)[0]
        elif statistic.th.text == SCRAPING_DAMAGE:
            jsonDict[SCRAPING_DAMAGE] = statistic.td.text.split(' ')[0].rstrip()
        elif statistic.th.text == SCRAPING_VELOCITY:
            jsonDict[SCRAPING_VELOCITY] = statistic.td.text.split(' ')[0].rstrip()
        elif statistic.th.text == SCRAPING_KNOCKBACK:
            jsonDict[SCRAPING_KNOCKBACK] = statistic.td.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()
        elif statistic.th.text == SCRAPING_AVAILABLE:
            jsonDict[SCRAPING_AVAILABLE] = (statistic.td.text.rstrip()).replace("  ", " ")
        elif statistic.th.text == SCRAPING_EFFECT:
            jsonDict[SCRAPING_EFFECT] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
        elif statistic.th.text == SCRAPING_TOOLTIP:
            if isArmor:
                jsonDict[SCRAPING_TOOLTIP] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.split("/")[0].rstrip()
            else:
                jsonDict[SCRAPING_TOOLTIP] = BeautifulSoup(str(statistic.td).replace("<br/>", ". "), 'html.parser').text.rstrip()
        elif statistic.th.text == SCRAPING_SELL:
            jsonDict[SCRAPING_SELL] = statistic.td.span["title"]
        elif statistic.th.text == SCRAPING_BASE_VELOCITY:
            jsonDict[SCRAPING_BASE_VELOCITY] = statistic.td.text.rstrip()
        elif statistic.th.text == SCRAPING_VELOCITY_MULTIPLIER:
            jsonDict[SCRAPING_VELOCITY_MULTIPLIER] = statistic.td.text.encode("ascii", "ignore").decode().rstrip() + "x"
        elif statistic.th.text == SCRAPING_MANA:
            jsonDict[SCRAPING_MANA] = statistic.td.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()
        elif statistic.th.text == SCRAPING_CRITICAL_CHANCE:
            jsonDict[SCRAPING_CRITICAL_CHANCE] = statistic.td.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()
        elif statistic.th.text == SCRAPING_DEFENSE:
            jsonDict[SCRAPING_DEFENSE] = statistic.td.text.split(" ")[0]
        elif statistic.th.text == SCRAPING_BODY_SLOT:
            jsonDict[SCRAPING_BODY_SLOT] = statistic.td.text
        elif statistic.th.text == SCRAPING_BONUS:
            jsonDict[SCRAPING_BONUS] = statistic.td.text
        elif statistic.th.text == SCRAPING_MAX_STACK:
            jsonDict[SCRAPING_MAX_STACK] = statistic.td.text.split("/")[0].encode("ascii", "ignore").decode().rstrip()

    #get toolpower for tools json
    toolPower = tableBox.find("ul", class_="toolpower")
    if toolPower:
        powerList = toolPower.find_all("li")
        for powerType in powerList:
            if(powerType["title"] == SCRAPING_PICKAXE_POWER):
                jsonDict[SCRAPING_PICKAXE_POWER] = powerType.text[1:].split(" ", 1)[0]
            elif(powerType["title"] == SCRAPING_HAMMER_POWER):
                jsonDict[SCRAPING_HAMMER_POWER] = powerType.text[1:].split(" ", 1)[0]
            elif(powerType["title"] == SCRAPING_AXE_POWER):
                jsonDict[SCRAPING_AXE_POWER] = powerType.text[1:].split(" ", 1)[0]
    #Check if optional parameter was given
    if usedIn:
        jsonDict[SCRAPING_USED_IN] = usedIn
    if isArmor and itemInstance:
        jsonDict[SCRAPING_SET_ID] = itemInstance[SCRAPING_SET_ID]
    jsonDict[SCRAPING_SOURCES] = SOURCE_SOURCES_DICT
    return jsonDict
