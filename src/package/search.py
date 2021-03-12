from .json_labels import *
# Search algorithms

NOT_FOUND = -1

def __binarySearching(searchList, searchValue, firstElement, lastElement):
    if (lastElement < firstElement):
        return NOT_FOUND

    middlePoint = int((firstElement+lastElement) / 2)

    if int(searchList[middlePoint][LABEL_ITEM_ID]) == int(searchValue):
        return searchList[middlePoint]
    elif int(searchList[middlePoint][LABEL_ITEM_ID]) < int(searchValue):
        return __binarySearching(searchList, searchValue, middlePoint+1, lastElement)
    else:
        return __binarySearching(searchList, searchValue, firstElement, middlePoint-1)

def binarySearch(searchList, searchValue):
    return __binarySearching(searchList, searchValue, 0, len(searchList))

