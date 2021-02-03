import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
parent_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
from scraping_tools import *
from json_manager import *

IMG_PATH = "img/{}.png"

itemList = LoadJSONFile(ITEM_FILE_PATH)

for itemInstance in itemList:
    if not os.path.isfile(IMG_PATH.format(itemInstance[SCRAPING_NAME].replace(" ", "_").replace("/", "_"))):
        print("{} not found on img path".format(itemInstance[SCRAPING_NAME]))