import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir) 
from json_manager import *

SETS_PATH_OUTPUT = GLOBAL_JSON_PATH + "items_armors.json"

itemArmors = LoadJSONFile(GLOBAL_JSON_PATH + "items_armors.json")
itemSets = LoadJSONFile(GLOBAL_JSON_PATH + "sets.json")

for armor in itemArmors:
    for set in itemSets:
        if armor["Name"] in set["Set Pieces"]:
            armor["Set ID"] = str(set["ID"])
            break
SaveJSONFile(SETS_PATH_OUTPUT, itemArmors)