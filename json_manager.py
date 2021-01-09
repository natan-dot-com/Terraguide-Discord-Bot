import json

ITEM_FILE_PATH = 'json/new_items.json' #only for this branch
RECIPE_FILE_PATH = 'json/recipes.json'
TABLE_FILE_PATH = 'json/tables.json'

def LoadJSONFile(JSONPath):
    with open(JSONPath) as newJSONFile:
        JSONData = json.load(newJSONFile)        
        return JSONData

