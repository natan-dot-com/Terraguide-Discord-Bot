import json

NOT_FOUND = -1

GLOBAL_JSON_PATH = "json/"
ITEM_FILE_PATH = "json/items.json"
RECIPE_FILE_PATH = "json/recipes.json"
TABLE_FILE_PATH = "json/tables.json"

def LoadJSONFile(JSONPath):
    try:
        with open(JSONPath) as JSONFile:
            print("File '" + JSONPath + "' found.")
            JSONData = json.load(JSONFile)        
    except IOError:
        print("Requested file '" + JSONPath + "' not found.")
        JSONData = []
    return JSONData

def SaveJSONFile(JSONPath, Structure):
    with open(JSONPath, "w") as newJSONFile:
        json.dump(Structure, newJSONFile, indent=4)
