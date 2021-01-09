#This generator doesn't work very well yet
#a comma will always be put at the final of JSON output which is not expected.

from asyncio.windows_events import NULL
import json
from json_manager import *

new_item = {
    "id": "",
    "name": "",
    "recipe1": "",
    "recipe2": "",
    "recipe3": "",
    "recipe4": "",
    "recipe5": "",
    "recipe6": ""
    }

NEW_ITEM_FILE_PATH = 'json/new_items.json'

def NextIndex(previousItemIndex):
    return previousItemIndex + 1

def CheckMissingIndex(previousItemIndex, itemInstance):
    if previousItemIndex == -1:
        return 0

    if NextIndex(previousItemIndex) != int(itemInstance['id']):
        return 1

newItem = open(NEW_ITEM_FILE_PATH, "w")

itemList = LoadJSONFile(ITEM_FILE_PATH)

previousItemIndex = -1

newItem.write("[\n")

for itemInstance in itemList:
    while CheckMissingIndex(previousItemIndex, itemInstance):
        json.dumps(new_item, indent=2)
        json.dump(new_item, newItem)
        newItem.write(",\n")
        previousItemIndex = previousItemIndex + 1

    previousItemIndex = int(itemInstance['id'])
    json.dumps(itemInstance, indent=2)
    json.dump(itemInstance, newItem)
    newItem.write(",\n")

newItem.write("]")
