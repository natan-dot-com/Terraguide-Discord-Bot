from .json_manager import *
from .json_labels import *
from .item_hash import *

ARG_NOT_FOUND = -1
ITEM_NOT_FOUND = -2
SET_NOT_FOUND = -3

botDescription = 'A terraria bot.'
botPrefix = 't.'
emojiPrefix = "t_"

# Thumbnail for UI output commands
helpThumbNail = 'https://img2.gratispng.com/20180326/ytq/kisspng-question-mark-clip-art-competition-5ab8be3d0288c7.3002224515220567650104.jpg'

# Color for UI output commands
craftColor = 0x0a850e
listColor = 0xe40101
helpColor = 0x000000

# Discord bot commands
helpCommand = botPrefix + "help"
craftCommand = botPrefix + "craft *Item Name*"
listCommand = botPrefix + "list *Something to Search*"
itemCommand = botPrefix + "item *Item Name*"
setCommand = botPrefix + "set *Set Name*"
rarityCommand = botPrefix + "rarity *rarity Name*"

# Command List description
commandList = {
    helpCommand: "Show this dialog",
    craftCommand: "Show all recipes for an item",
    listCommand: "Find all items that contains the input word",
    itemCommand: "Show informations about an item",
    setCommand: "Show informations about a set",
    rarityCommand: "Show informations about a Rarity Tier. If no parameters were given to this command, it shows all rarity tiers information"
}

pageSize = 12
reactionTimeOut = 30.0
pageAlert = "React to this message to switch between pages!\n" + "Page {}/{}"

#BotToken = "MjQ2NTExOTcxMDY5ODUzNjk3.WCVcKQ.quxR1uO0TUb6UQPhvLYzqoApHBI"
BotToken = "Nzk2MDY1OTI0NzU1MDk1NTg0.X_SgKg.8UNAsVGPDnbS2nMc40LrpuoepTI"

def loadDependencies(jsonList, hashSize=ITEMS_HASH_SIZE, label=LABEL_NAME):
    itemFilePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + MAIN_NAME_FILE + JSON_EXT
    itemHash = hashTable(hashSize, label)
    itemHash = initializeHashTable(itemHash, jsonList)

    return itemHash

