from .json_labels import *
from .json_manager import GLOBAL_IMAGE_PATH
from .bot_config import *
from colorthief import ColorThief
from colormap import rgb2hex

def getCommandArgumentList(commandArgument):
    commandArgumentList = []
    for argument in commandArgument[1:]:
        if BOT_CONFIG_FLAG_PREFIX + argument in commandArgumentList:
            return ERROR_INVALID_FLAG
        elif argument == FLAG_PRIVATE[1]:
            commandArgumentList.append(FLAG_PRIVATE)
        elif argument == FLAG_LINEAR[1]:
            commandArgumentList.append(FLAG_LINEAR)
        elif not BOT_CONFIG_FLAG_PREFIX + argument in commandFlagList:
            return ERROR_INVALID_FLAG
    return commandArgumentList

def getCommandArguments(args):
    commandArgumentList = []
    commandStringInput = ""
    if args:
        # If first argument given is flag
        if args[0][0] == "-":
            if len(args) > 1:
                commandStringInput = " ".join(args[1:])
            commandArgumentList = getCommandArgumentList(args[0])
        else:
            commandStringInput = " ".join(args)
 
    return commandArgumentList, commandStringInput

def pickDominantColor(imageFilename, imagePath=GLOBAL_IMAGE_PATH):
    dominant_color = ColorThief(imagePath + imageFilename).get_color(quality=1)
    hexcode = "0x" + rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2])[1::]
    return int(hexcode, 16)

def getGuildEmojiByName(emojiName, guildEmojis):
    for guildEmoji in guildEmojis:
        if emojiName == str(guildEmoji.name):
            return guildEmoji
    return ERROR_EMOJI_NOT_FOUND
