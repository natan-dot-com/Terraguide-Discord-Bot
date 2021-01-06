import json

ITEM_FILENAME = 'json/items.json'
RECIPE_FILENAME = 'json/recipes.json'
TABLE_FILE = 'json/tables.json'

def openJSONFile(JSONFilename):
    with open(JSONFilename) as JSONFile:
        JSONData = json.load(JSONFile)
        return JSONData
