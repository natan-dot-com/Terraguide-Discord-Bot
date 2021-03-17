from .json_manager import *
from .json_labels import *
from .item_hash import *

ARG_NOT_FOUND = -1
ITEM_NOT_FOUND = -2

botDescription = 'A terraria bot.'
botPrefix = 't.'

#Thumbnail for UI output commands
craftThumbNail = 'https://art.pixilart.com/7b7bd37bb742cd4.png'
listThumbNail = 'https://cdn2.iconfinder.com/data/icons/font-awesome/1792/search-512.png'
helpThumbNail = 'https://img2.gratispng.com/20180326/ytq/kisspng-question-mark-clip-art-competition-5ab8be3d0288c7.3002224515220567650104.jpg'

#Color for UI output commands
craftColor = 0x0a850e
listColor = 0xe40101
helpColor = 0x000000

#Command List
commandList = {
    botPrefix + "help": "Show this dialog",
    botPrefix + "craft *Item Name*": "Show all recipes for an item",
    botPrefix + "list *Something to Search*": "Find all items that contains the input word",
    botPrefix + "item *Item Name*": "Show informations about an item"
}

pageSize = 12
reactionTimeOut = 30.0


def loadDependencies(itemList):
    itemFilePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + MAIN_NAME_FILE + JSON_EXT
    itemHash = hashTable(ITEMS_HASH_SIZE, LABEL_NAME)
    itemHash = initializeHashTable(itemHash, itemList)

    return itemHash

