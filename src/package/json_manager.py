from .json_labels import *
import json

NOT_FOUND = -1

GLOBAL_JSON_PATH = "data/json/"
GLOBAL_IMAGE_PATH = "data/img_sprites/"

DIR_ID_REFERENCES = "id_references/"
DIR_ITEMS_DATA = "items_data/"
DIR_NPC_DATA = "npc_data/"

# Loads a structure inside a JSON file
def LoadJSONFile(JSONPath):
    try:
        with open(JSONPath) as JSONFile:
            print("File '" + JSONPath + "' found.")
            JSONData = json.load(JSONFile)        
    except IOError:
        print("Requested file '" + JSONPath + "' not found.")
        JSONData = []
    return JSONData

# Saves a structure in a JSON file
def SaveJSONFile(JSONPath, Structure):
    with open(JSONPath, "w") as newJSONFile:
        json.dump(Structure, newJSONFile, indent=4)
        
