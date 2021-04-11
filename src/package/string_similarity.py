import discord
import Levenshtein as lev
from .json_labels import LABEL_NAME
from .embed_functions import embedSetFooter, embedInsertField

TUPLE_RATIO_INDEX = 0
TUPLE_STRING_INDEX = 1

def getSimilarStrings(typedString, itemList, maxSamples=4, label=LABEL_NAME):
    dissimilarityList = []

    # Gets Levenshtein ratio from each string in itemList
    for itemInstance in itemList:

        # (levRatio, respectiveString) tuple
        infoTuple = (lev.ratio(typedString.lower(), itemInstance[label].lower()), itemInstance[label])
        dissimilarityList.append(infoTuple)

    # Sort list in descending order
    dissimilarityList.sort(key=lambda tup: tup[TUPLE_RATIO_INDEX], reverse=True)

    # Gets the most similar string only if its similarity ratio is greater or equal 60% 
    similarStrings = []
    numberIdentifier = 0
    if dissimilarityList[0][TUPLE_RATIO_INDEX] >= 0.6:
        numberIdentifier += 1

        # stringTuple = (<Identifier>, <Item Name>)
        stringTuple = (str(numberIdentifier), dissimilarityList[0][TUPLE_STRING_INDEX])
        similarStrings.append(stringTuple)


    # Gets other similar strings with similarity ratio greater than 82.5%
    # maxSamples acts as a limit number of words that can be taken
    for i in range(1, maxSamples):
        if dissimilarityList[i][TUPLE_RATIO_INDEX] >= 0.825:
            numberIdentifier += 1

            # stringTuple = (<Identifier>, <Item Name>)
            stringTuple = (str(numberIdentifier), dissimilarityList[i][TUPLE_STRING_INDEX])
            similarStrings.append(stringTuple)
        else:
            break
    return similarStrings

def getSimilarStringEmbed(titleMessage, inputString, itemList, label=LABEL_NAME):
    errorEmbed = discord.Embed(title=titleMessage, color=0xFFFFFF)

    notFoundTitle =  "Didn't you mean...?"
    notFoundMessage = ""
    similarStrings = getSimilarStrings(inputString, itemList, label=label)

    NUMBER_IDENTIFIER = 0
    ITEM_NAME = 1
    if similarStrings:
        for string in similarStrings:
            notFoundMessage += "**" + string[NUMBER_IDENTIFIER] + ".** " + string[ITEM_NAME] + "\n"
    else:
        notFoundMessage = "Couldn't retrieve any suggestions from data base."
    embedInsertField(errorEmbed, notFoundMessage, notFoundTitle, inline=False)

    footnoteString = "Type which number corresponds to what you were supposed to mean. If none, type '0'."
    embedSetFooter(errorEmbed, footnoteString)
    return errorEmbed, similarStrings
