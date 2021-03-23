from .json_labels import *
from .json_manager import GLOBAL_IMAGE_PATH
from .bot_config import *
from colorthief import ColorThief
from colormap import rgb2hex

def getCommandArgumentList(commandArgument):
    commandArgumentList = []
    for argument in commandArgument[1:]:
        if argumentPrefix + argument in commandArgumentList:
            return INVALID_FLAG
        elif argument == sendDM[1]:
            commandArgumentList.append(sendDM)
        elif argument == sendLinear[1]:
            commandArgumentList.append(sendLinear)
        elif not argumentPrefix + argument in commandFlagList:
            return INVALID_FLAG
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
    return EMOJI_NOT_FOUND
