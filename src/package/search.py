from .json_labels import *

# Search algorithms
NOT_FOUND = -1

def __binarySearching(searchList, searchValue, firstElement, lastElement, label=LABEL_ITEM_ID):
    if (lastElement < firstElement):
        return NOT_FOUND

    middlePoint = int((firstElement+lastElement) / 2)

    if int(searchList[middlePoint][label]) == int(searchValue):
        return searchList[middlePoint]
    elif int(searchList[middlePoint][label]) < int(searchValue):
        return __binarySearching(searchList, searchValue, middlePoint+1, lastElement, label=label)
    else:
        return __binarySearching(searchList, searchValue, firstElement, middlePoint-1, label=label)

def binarySearch(searchList, searchValue, label=LABEL_ITEM_ID):
    return __binarySearching(searchList, searchValue, 0, len(searchList), label=label)

def linearSearch(searchList, searchIndex, searchValue):
    for searchItem in searchList:
        if searchItem[searchIndex].lower() == searchValue:
            return searchItem
    return NOT_FOUND

