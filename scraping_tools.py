import requests

# General labels
SCRAPING_ID = "ID"
SCRAPING_TYPE = "Type"
SCRAPING_ITEM_ID = "Item ID"
SCRAPING_NAME = "Name"
SCRAPING_RARITY = "Rarity"
SCRAPING_USE_TIME = "Use Time"
SCRAPING_VELOCITY = "Velocity"
SCRAPING_TOOL_SPEED = "Tool Speed"
SCRAPING_PICKAXE_POWER = "Pickaxe Power"
SCRAPING_HAMMER_POWER = "Hammer Power"
SCRAPING_AXE_POWER = "Axe Power"
SCRAPING_FISHING_POWER = "Fishing Power"
SCRAPING_SET_ID = "Set ID"
SCRAPING_DEFENSE = "Defense"
SCRAPING_BODY_SLOT = "Body Slot"
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
SCRAPING_CRITICAL_CHANCE = "Critical Chance"
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
