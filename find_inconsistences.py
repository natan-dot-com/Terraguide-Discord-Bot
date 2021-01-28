#temporary file for testing

from json_manager import *
from tools import *

ITEM_FILE_NAME = "items_Armors.json"
CATEGORY = "Armor"

itemList = LoadJSONFile(ITEM_FILE_PATH)
toolList = LoadJSONFile(GLOBAL_JSON_PATH + ITEM_FILE_NAME)

count = 0
for itemInstance in itemList:
    if itemInstance["Type"] == CATEGORY:
        if searchByName(toolList, itemInstance['Name']) == NOT_FOUND:
            print("{} not found on category json".format(itemInstance["Name"]))
            if itemInstance["Type"] != CATEGORY:
                print("{} category isn't right".format(itemInstance["Name"]))
        count += 1
print("{} instances of items found".format(count))
count = 0
for toolInstance in toolList:
    if searchByName(itemList, toolInstance['Name']) == NOT_FOUND:
            print("{} not found on item json".format(toolInstance["Name"]))
    count += 1
print("{} instances of armors found".format(count))