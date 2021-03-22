from .json_labels import *
from .json_manager import GLOBAL_IMAGE_PATH
from colorthief import ColorThief
from colormap import rgb2hex

EMOJI_NOT_FOUND = -1

def pickDominantColor(imageFilename, imagePath=GLOBAL_IMAGE_PATH):
    dominant_color = ColorThief(imagePath + imageFilename).get_color(quality=1)
    hexcode = "0x" + rgb2hex(dominant_color[0], dominant_color[1], dominant_color[2])[1::]
    return int(hexcode, 16)

def getGuildEmojiByName(emojiName, guildEmojis):
    for guildEmoji in guildEmojis:
        if emojiName == str(guildEmoji.name):
            return guildEmoji
    return EMOJI_NOT_FOUND
