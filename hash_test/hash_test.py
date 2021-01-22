from item_hash import *
from json_manager import *

ITEMS_DICT_STRING_INDEX = 'name'
ITEMS_DICT_INDEX_TO_RETURN = 'id'
ITEMS_TABLE_SIZE = 8192

itemList = LoadJSONFile('items.json')
hashMap = hashTable(ITEMS_TABLE_SIZE, ITEMS_DICT_STRING_INDEX)
for itemInstance in itemList:
    hashMap.hashString(itemInstance[ITEMS_DICT_STRING_INDEX], itemInstance)

while True:
    itemName = input('>>> Item name: ')
    respectiveID = hashMap.dehashString(itemName, ITEMS_DICT_INDEX_TO_RETURN)
    if respectiveID != NOT_FOUND:
        print("Item ID: " + respectiveID)
    else:
        print("Not found.")
