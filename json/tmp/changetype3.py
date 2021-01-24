import json
import re
from bs4 import BeautifulSoup
import requests
from item_hash import *

with open('items.json') as infile:
    itemList = json.load(infile)

for itemInstance in itemList:
    if re.search("Dresser$", itemInstance['name']):
        print(itemInstance['name'])
        itemInstance['type'] = "Storage"

with open('items.json', "w+") as outfile:
    json.dump(itemList, outfile, indent=4)
