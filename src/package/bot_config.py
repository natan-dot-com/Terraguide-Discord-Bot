from .json_manager import *
from .json_labels import *
from .item_hash import *

# Error return values
ERROR_ARG_NOT_FOUND = -1
ERROR_ITEM_NOT_FOUND = -2
ERROR_SET_NOT_FOUND = -3
ERROR_DATASET_INCONSISTENCE = -4
ERROR_INVALID_FLAG = -5
ERROR_EMOJI_NOT_FOUND = -6


# Bot general constants
BOT_CONFIG_DESCRIPTION = ''
BOT_CONFIG_PREFIX = 't.'
BOT_CONFIG_FLAG_PREFIX = "-"


# Command flags related stuff

# Command flags definition
FLAG_PRIVATE = BOT_CONFIG_FLAG_PREFIX + "p"
FLAG_LINEAR = BOT_CONFIG_FLAG_PREFIX + "l"

# Command flag messages
FLAG_TITLE_LABEL = "Command flags:"
FLAG_ERROR_MESSAGE = "Couldn't solve specified flags. Review the previous command or enter t.help for\
further information."

# Command flags list
commandFlagList = [
    FLAG_PRIVATE, FLAG_LINEAR
]


# t.help command related stuff

# Help messages
HELP_EMBED_TITLE = "Terraguide Help Documentation:"

# Command flags description
flagDescriptionList = [
    "**" + FLAG_PRIVATE + "** (private): Sends the current output as a private message to the author.",
    "**" + FLAG_LINEAR + "** (linear): Sends the current output as pageless (potential spam alert)."
]

COMMAND_WAIT_MESSAGE_TIMEOUT = 15.0

COMMAND_SUBMESSAGE = "See ``t.help`` for further information."
COMMAND_EMPTY_ERROR_MESSAGE = "**{}**: {}, please specify which instance is wanted to be searched.\n" + COMMAND_SUBMESSAGE
COMMAND_NOT_FOUND_MESSAGE = "**{}**: Couldn't retrieve given command.\n" + COMMAND_SUBMESSAGE

# Embed page related constants
PAGE_DEFAULT_SIZE = 12
PAGE_NPC_ITEMS_COUNT = 5
PAGE_REACTION_TIMEOUT = 30.0
PAGE_ALERT_MESSAGE = "React to this message to switch between pages!\n" + "Page {}/{}"


# Emojis related constants
EMOJI_WHITE_CHECK_MARK = "✅"

# Function names constants

NPC_FUNCTION = "npc"
RARITY_FUNCTION = "rarity"
ITEM_FUNCTION = "item"
SET_FUNCTION = "set"
CRAFT_FUNCTION = "craft"
BAGDROP_FUNCTION = "bagdrop"
SELL_FUNCTION = "sell"

def loadDependencies(jsonList: list, hashSize=ITEMS_HASH_SIZE, label=LABEL_NAME) -> hashTable:
    itemFilePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + MAIN_NAME_FILE + JSON_EXT
    itemHash = hashTable(hashSize, label)
    itemHash = initializeHashTable(itemHash, jsonList)
    return itemHash
