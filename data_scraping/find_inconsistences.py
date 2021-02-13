#temporary file for testing

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from scraping_tools import *
from json_manager import *
from tools import *

ITEM_FILE_NAME = "items_furnitures.json"
CATEGORY = "Furniture"

itemList = LoadJSONFile(GLOBAL_JSON_PATH + MAIN_NAME_FILE + JSON_EXT)
toolList = LoadJSONFile(GLOBAL_JSON_PATH + ITEM_FILE_NAME)

count = 0
listID = []
for itemInstance in itemList:
    if itemInstance[SCRAPING_TYPE] == CATEGORY:

        if itemInstance[SCRAPING_ID] in listID:
            print("{} repeated in item json".format(itemInstance[SCRAPING_NAME]))
        listID.append(itemInstance[SCRAPING_ID])

        if searchByName(toolList, itemInstance[SCRAPING_NAME]) == NOT_FOUND:
            print("{} not found on category json".format(itemInstance[SCRAPING_NAME]))
            if itemInstance[SCRAPING_TYPE] != CATEGORY:
                print("{} category isn't right".format(itemInstance[SCRAPING_NAME]))

        count += 1
print("{} instances of items found".format(count))
count = 0
listID = []
for toolInstance in toolList:
    if toolInstance[SCRAPING_ITEM_ID] in listID:
        print("{} repeated in category json".format(toolInstance[SCRAPING_NAME]))
    listID.append(toolInstance[SCRAPING_ITEM_ID])

    if searchByName(itemList, toolInstance[SCRAPING_NAME]) == NOT_FOUND:
            print("{} not found on item json".format(toolInstance[SCRAPING_NAME]))
            
    count += 1
print("{} instances of {} found".format(count, CATEGORY))