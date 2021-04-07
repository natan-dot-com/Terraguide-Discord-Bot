from .json_labels import *
from .json_manager import GLOBAL_IMAGE_PATH
from .bot_config import *
from colorthief import ColorThief
from colormap import rgb2hex

# Get all input flags
def getCommandFlagList(commandArgument):
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

# Returns a list of flags and the input string
def getCommandArguments(args):
    commandArgumentList = []
    commandStringInput = ""
    if args:
        # If first argument given is flag
        if args[0][0] == "-":
            if len(args) > 1:
                commandStringInput = " ".join(args[1:])
            commandArgumentList = getCommandFlagList(args[0])
        else:
            commandStringInput = " ".join(args)
 
    return commandArgumentList, commandStringInput

# Library function to get the dominant color of a given file
def pickDominantColor(imageFilename, imagePath=GLOBAL_IMAGE_PATH):
    dominant_color = ColorThief(imagePath + imageFilename).get_color(quality=1)
    hexcode = "0x" + rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2])[1::]
    return int(hexcode, 16)

# Get the image extension of a given file
def getImageExt(imageFilePath, imageFileName):
    file = None
    try:
        file = open(imageFilePath + imageFileName + STATIC_IMAGE_EXT)
        imageExt = STATIC_IMAGE_EXT
    except IOError:
        file = open(imageFilePath + imageFileName + DYNAMIC_IMAGE_EXT)
        imageExt = DYNAMIC_IMAGE_EXT
    finally:
        file.close()
        return imageExt
    
# Get an existent emoji on server by its name
def getGuildEmojiByName(emojiName, guildEmojis):
    for guildEmoji in guildEmojis:
        if emojiName == str(guildEmoji.name):
            return guildEmoji
    return ERROR_EMOJI_NOT_FOUND
