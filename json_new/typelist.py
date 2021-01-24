import json
import re
from bs4 import BeautifulSoup
import requests
from item_hash import *


typeList = []
with open('items.json') as infile:
    itemList = json.load(infile)

for itemInstance in itemList:
    if itemInstance['type'] not in typeList:
        typeList.append(itemInstance['type'])

inputType = input(">>> Type: ")

if inputType == "cmd.counter":
    print("Type counter: " + str(len(typeList)))
    for typeInstance in typeList:
        counter = 0
        for itemInstance in itemList:
            if itemInstance['type'] == typeInstance:
                counter += 1
        print("Type \"" + typeInstance + "\": " + str(counter))

for itemInstance in itemList:
    if itemInstance['type'] == inputType:
        print("- " + itemInstance['id'] + ": " + itemInstance['name'])
