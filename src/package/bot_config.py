from .json_manager import *
from .json_labels import *
from .item_hash import *

ARG_NOT_FOUND = -1
ITEM_NOT_FOUND = -2
SET_NOT_FOUND = -3
DATASET_INCONSISTENCE = -4

botDescription = 'A terraria bot.'
botPrefix = 't.'

# Thumbnail for UI output commands
helpThumbNail = 'https://img2.gratispng.com/20180326/ytq/kisspng-question-mark-clip-art-competition-5ab8be3d0288c7.3002224515220567650104.jpg'

# Color for UI output commands
craftColor = 0x0a850e
listColor = 0xe40101
helpColor = 0x000000

#Emojis
whiteCheckMark = "✅"

# Discord bot commands
helpCommand = botPrefix + "help"
craftCommand = botPrefix + "craft 'Item Name'"
listCommand = botPrefix + "list 'Something to Search'"
itemCommand = botPrefix + "item 'Item Name'"
setCommand = botPrefix + "set 'Set Name'"
rarityCommand = botPrefix + "rarity 'rarity Name'"

# Command List description
commandList = {
    helpCommand: "Opens the command help box.",
    craftCommand: "Shows every crafting recipe for a given argument.",
    listCommand: "Searches for all related items inside the dataset based on a given argument.",
    itemCommand: "Points every information about a given item such as its crafting recipes, its general stats and where does\
    it can drop.",
    setCommand: "Displays every information about a given armor set.",
    rarityCommand: "Displays a brief description about the specified rarity tier. All tiers can be displayed by giving\
    no arguments to the command."
}

argumentsLabel = "Command flags:"
argumentsDescription = "**-p** (private): Sends the current output as a private message to the author."

# Commands Arguments
sendDM = "-p"

argumentListDescription = {
    sendDM: "Send a private message to de user"
}

pageSize = 12
npcPageItemsCount = 5
reactionTimeOut = 30.0
pageAlert = "React to this message to switch between pages!\n" + "Page {}/{}"

#BotToken = "MjQ2NTExOTcxMDY5ODUzNjk3.WCVcKQ.quxR1uO0TUb6UQPhvLYzqoApHBI"
BotToken = "Nzk2MDY1OTI0NzU1MDk1NTg0.X_SgKg.8UNAsVGPDnbS2nMc40LrpuoepTI"

def loadDependencies(jsonList, hashSize=ITEMS_HASH_SIZE, label=LABEL_NAME):
    itemFilePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + MAIN_NAME_FILE + JSON_EXT
    itemHash = hashTable(hashSize, label)
    itemHash = initializeHashTable(itemHash, jsonList)

    return itemHash

