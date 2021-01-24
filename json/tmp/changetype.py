import json
import re
from bs4 import BeautifulSoup
import requests
from item_hash import *


with open('items.json') as infile:
    itemList = json.load(infile)

targetType = input(">>> Target type: ")
newType = input(">>> New type: ")
for itemInstance in itemList:
    if itemInstance['type'] == targetType:
        itemInstance['type'] = newType

with open('items.json', "w+") as outfile:
    json.dump(itemList, outfile, indent=4)

