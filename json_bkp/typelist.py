import json
import re
from bs4 import BeautifulSoup
import requests
from item_hash import *


typeList = []
with open('items.json') as infile:
    itemList = json.load(infile)

for itemInstance in itemList:
    if itemInstance['Type'] not in typeList:
        typeList.append(itemInstance['Type'])

inputType = input(">>> Type: ")

if inputType == "cmd.counter":
    print("Type counter: " + str(len(typeList)))
    for typeInstance in typeList:
        counter = 0
        for itemInstance in itemList:
            if itemInstance['Type'] == typeInstance:
                counter += 1
        print("Type \"" + typeInstance + "\": " + str(counter))

for itemInstance in itemList:
    if itemInstance['Type'] == inputType:
        print("- " + itemInstance['ID'] + ": " + itemInstance['Name'])
