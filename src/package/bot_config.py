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
BOT_CONFIG_DESCRIPTION = 'A terraria bot.'
BOT_CONFIG_PREFIX = 't.'
BOT_CONFIG_FLAG_PREFIX = "-"
#BOT_TOKEN = "MjQ2NTExOTcxMDY5ODUzNjk3.WCVcKQ.quxR1uO0TUb6UQPhvLYzqoApHBI"
BOT_TOKEN = "Nzk2MDY1OTI0NzU1MDk1NTg0.X_SgKg.8UNAsVGPDnbS2nMc40LrpuoepTI"


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
HELP_EMBED_TITLE = "Terraria Bot Help Documentation:"
HELP_INTRODUCTION_TITLE = "Usage: [COMMAND] [FLAGS (optional)] [ARGUMENTS]"
HELP_INTRODUCTION_DESC = "Multiple flags should be written together of each other (e.g. -abcd). As an optional\
 factor, flags can be ignored simply by putting none at the current command."

# Discord bot commands constants
COMMAND_HELP = BOT_CONFIG_PREFIX + "help"
COMMAND_CRAFT = BOT_CONFIG_PREFIX + "craft 'Item Name'"
COMMAND_LIST = BOT_CONFIG_PREFIX + "list 'Something to Search'"
COMMAND_ITEM = BOT_CONFIG_PREFIX + "item 'Item Name'"
COMMAND_SET = BOT_CONFIG_PREFIX + "set 'Set Name'"
COMMAND_RARITY = BOT_CONFIG_PREFIX + "rarity 'Rarity Name'"

# Commands description
commandDict = {
    COMMAND_HELP: "Opens the command help box.",
    COMMAND_CRAFT: "Shows every crafting recipe for a given argument.",
    COMMAND_LIST: "Searches for all related items inside the dataset based on a given argument.",
    COMMAND_ITEM: "Points every information about a given item such as its crafting recipes, its general stats and where does\
 it can drop.",
    COMMAND_SET: "Displays every information about a given armor set.",
    COMMAND_RARITY: "Displays a brief description about the specified rarity tier. All tiers can be displayed by giving\
 no arguments to the command."
}

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

def loadDependencies(jsonList: list, hashSize=ITEMS_HASH_SIZE, label=LABEL_NAME) -> hashTable:
    itemFilePath = GLOBAL_JSON_PATH + DIR_ID_REFERENCES + MAIN_NAME_FILE + JSON_EXT
    itemHash = hashTable(hashSize, label)
    itemHash = initializeHashTable(itemHash, jsonList)
    return itemHash
