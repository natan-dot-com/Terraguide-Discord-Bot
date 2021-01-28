import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
from scraping_tools import *
from json_manager import *

SETS_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_armors.json"

itemArmors = LoadJSONFile(GLOBAL_JSON_PATH + "items_armors.json")
itemSets = LoadJSONFile(GLOBAL_JSON_PATH + "sets.json")

for armor in itemArmors:
    for set in itemSets:
        if armor[SCRAPING_NAME] in set[SCRAPING_SET_PIECES]:
            armor[SCRAPING_SET_ID] = str(set[SCRAPING_ID])
            break
SaveJSONFile(SETS_PATH_OUTPUT, itemArmors)