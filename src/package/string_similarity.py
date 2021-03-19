import numpy as np
import Levenshtein as lev
from .json_labels import LABEL_NAME

TUPLE_RATIO_INDEX = 0
TUPLE_STRING_INDEX = 1

def getSimilarStrings(typedString, itemList, maxSamples=4):
    dissimilarityList = []

    # Gets Levenshtein ratio from each string in itemList
    for itemInstance in itemList:

        # (levRatio, respectiveString) tuple
        infoTuple = (lev.ratio(typedString.lower(), itemInstance[LABEL_NAME].lower()), itemInstance[LABEL_NAME])
        dissimilarityList.append(infoTuple)

    # Sort list in descending order
    dissimilarityList.sort(key=lambda tup: tup[TUPLE_RATIO_INDEX], reverse=True)

    # Gets the most similar string only if its similarity ratio is greater or equal 60% 
    similarStrings = []
    if dissimilarityList[0][TUPLE_RATIO_INDEX] >= 0.6:
        similarStrings.append(dissimilarityList[0][TUPLE_STRING_INDEX])

    # Gets other similar strings with similarity ratio greater than 82.5%
    # maxSamples acts as a limit number of words that can be taken
    for i in range(1, maxSamples):
        if dissimilarityList[i][TUPLE_RATIO_INDEX] >= 0.825:
            similarStrings.append(dissimilarityList[i][TUPLE_STRING_INDEX])
        else:
            break
    return similarStrings
