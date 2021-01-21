import json

ITEM_FILE_PATH = 'json/items.json'
RECIPE_FILE_PATH = 'json/recipes.json'
TABLE_FILE_PATH = 'json/tables.json'

def LoadJSONFile(JSONPath):
    with open(JSONPath) as JSONFile:
        JSONData = json.load(JSONFile)        
        return JSONData

def SaveJSONFile(JSONPath, Structure):
    with open(JSONPath, "w") as newJSONFile:
        json.dump(Structure, newJSONFile, indent=2)
